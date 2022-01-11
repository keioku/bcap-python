import socket
import struct
from threading import RLock
from typing import Tuple
from .b_cap_exception import HResult, BCapException
from .b_cap_converter import BCapConverter
from .b_cap_socket import BCapSocket


class BCapUdp(BCapSocket):

    _RETRY_MIN = 1
    _RETRY_MAX = 7
    _MAX_PACKET_SIZE = 504

    def __init__(self, should_return_hr: bool):
        self._sock = None
        self._lock = RLock()
        self._bcap_converter = BCapConverter(False, should_return_hr)
        self._retry = 1

    def connect(self, endpoint: str, timeout: float, retry: int) -> None:
        with self._lock:
            try:
                self.disconnect()
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._host, self._port = BCapConverter.parse_endpoint(endpoint)
                self.set_timeout(timeout)
                self.set_retry(retry)
            except Exception as e:
                self.disconnect()
                raise e

    def disconnect(self):
        with self._lock:
            self._serial = 1
            self._version = 1
            if self._sock:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass

                self._sock.close()
                self._sock = None

    def set_timeout(self, timeout: float):
        with self._lock:
            self._sock.settimeout(timeout)

    def get_timeout(self) -> float:
        return self._sock.gettimeout()

    def set_retry(self, retry: int) -> None:
        if retry < BCapUdp._RETRY_MIN or retry > BCapUdp._RETRY_MAX:
            raise ValueError()
        self._retry = retry

    def set_compression(self, enable: bool, level=-1):
        raise NotImplementedError()

    def request(self, func_id: int, args: list) -> any:

        retry = self._serial
        retry_count = 0

        with self._lock:
            while True:
                try:
                    serial = self._serial
                    self._send(serial, retry, func_id, args)
                    if self._serial >= 0xFFFF:
                        self._serial = 1
                    else:
                        self._serial += 1
                    (hr, deserialized_result) = self._recv(serial)
                    return self._bcap_converter.create_response_object(
                        hr, deserialized_result
                    )
                except BCapException:
                    raise
                except Exception:
                    retry_count += 1
                    if retry_count > self._retry:
                        raise BCapException(
                            HResult.E_FAIL, "The number of retries has been exceeded."
                        )

    def _send(self, serial: int, retry: int, func_id: int, args: list) -> None:
        serialized_packet = self._bcap_converter.serialize(serial, retry, func_id, args)
        message_length = len(serialized_packet)
        if message_length > BCapUdp._MAX_PACKET_SIZE:
            raise BCapException(
                HResult.E_INVALID_PACKET,
                "Serialized packet size is {0} bytes. In the case of UDP, the maximum value is {1} bytes".format(
                    message_length, BCapUdp._MAX_PACKET_SIZE
                ),
            )

        self._sock.sendto(serialized_packet, (self._host, self._port))

    def _recv(self, serial: int) -> Tuple[int, any]:
        while True:
            data, address = self._sock.recvfrom(65565)
            if address[0] != self._host or address[1] != self._port:
                continue

            (
                recv_serial,
                version,
                hr,
                deserialized_args,
            ) = self._bcap_converter.deserialize(data)

            if (recv_serial == serial) and (hr != HResult.S_EXECUTING):
                break

        if deserialized_args is None:
            return (hr, None)

        return (hr, deserialized_args[0])
