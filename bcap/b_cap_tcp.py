import socket
import struct
from threading import RLock
from typing import Tuple
from .b_cap_exception import HResult
from .b_cap_converter import BCapConverter
from .b_cap_socket import BCapSocket


class BCapTcp(BCapSocket):
    def __init__(self, should_return_hr: bool):
        self._version = 1
        self._sock = None
        self._lock = RLock()
        self._bcap_converter = BCapConverter(True, should_return_hr)
        self._recv_buffer = []
        self._send_flags = 0

        if hasattr(socket, "MSG_NOSIGNAL"):
            self._send_flags |= socket.MSG_NOSIGNAL

    def connect(self, endpoint: str, timeout: float, retry: int) -> None:
        with self._lock:
            try:
                self.disconnect()
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.set_timeout(timeout)
                host, port = BCapConverter.parse_endpoint(endpoint)
                self._sock.connect((host, port))
            except Exception as e:
                self.disconnect()
                raise e

    def disconnect(self) -> None:
        with self._lock:
            self._serial = 1
            if self._sock:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass

                self._sock.close()
                self._sock = None

    def set_timeout(self, timeout: float) -> None:
        with self._lock:
            self._sock.settimeout(timeout)

    def get_timeout(self) -> float:
        return self._sock.gettimeout()

    def set_retry(self, retry: int) -> None:
        raise NotImplementedError()

    def set_compression(self, enable: bool, level: int = -1) -> None:
        with self._lock:
            self._bcap_converter.set_compression_parameters(enable, level)

    def request(self, func_id: int, args: list) -> any:
        with self._lock:
            serial = self._serial
            self._send(serial, self._version, func_id, args)
            if self._serial >= 0xFFFF:
                self._serial = 1
            else:
                self._serial += 1

            (hr, deserialized_result) = self._recv(serial)

            return self._bcap_converter.create_response_object(hr, deserialized_result)

    def _send(self, serial: int, version: int, func_id: int, args: list) -> None:
        serialized_packet = self._bcap_converter.serialize(
            serial, version, func_id, args
        )
        self._sock.sendall(serialized_packet, self._send_flags)

    def _recv(self, serial: int) -> Tuple[int, any]:
        recv_buffer = b""

        while True:
            buffer_size = len(recv_buffer)
            if buffer_size < 1:
                recv_buffer = self._sock.recv(1)

            if recv_buffer[:1] != BCapConverter.BCAP_SOH:
                # Can not receive b-CAP SOH.
                recv_buffer = recv_buffer[1:]
                continue

            buffer_size = len(recv_buffer)
            if buffer_size < 5:
                recv_buffer = b"".join([recv_buffer, self._sock.recv(5 - buffer_size)])

            # Receive b-CAP message length.
            (message_length,) = struct.unpack("<I", recv_buffer[1:5])

            buffer_size = len(recv_buffer)
            if buffer_size < message_length:
                recv_buffer = b"".join(
                    [recv_buffer, self._sock.recv(message_length - buffer_size)]
                )

            if recv_buffer[-1:] != BCapConverter.BCAP_EOT:
                # Can not receive b-CAP EOT.
                continue

            (
                recv_serial,
                version,
                hr,
                deserialized_args,
            ) = self._bcap_converter.deserialize(recv_buffer)

            recv_buffer = b""
            if (recv_serial == serial) and (hr != HResult.S_EXECUTING):
                break

        if deserialized_args is None:
            return (hr, None)

        return (hr, deserialized_args[0])
