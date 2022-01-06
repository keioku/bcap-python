import ctypes
import io
import struct
import zlib
from datetime import datetime
from typing import Union, Tuple
from urllib.parse import urlsplit
from .b_cap_exception import BCapException, HResult


class VarType:
    VT_EMPTY = 0
    VT_NULL = 1
    VT_I2 = 2
    VT_I4 = 3
    VT_R4 = 4
    VT_R8 = 5
    VT_CY = 6
    VT_DATE = 7
    VT_BSTR = 8
    VT_DISPATCH = 9
    VT_ERROR = 10
    VT_BOOL = 11
    VT_VARIANT = 12
    VT_UNKNOWN = 13
    VT_DECIMAL = 14
    VT_I1 = 16
    VT_UI1 = 17
    VT_UI2 = 18
    VT_UI4 = 19
    VT_I8 = 20
    VT_UI8 = 21
    VT_INT = 22
    VT_UINT = 23
    VT_VOID = 24
    VT_HRESULT = 25
    VT_PTR = 26
    VT_SAFEARRAY = 27
    VT_CARRAY = 28
    VT_USERDEFINED = 29
    VT_LPSTR = 30
    VT_LPWSTR = 31
    VT_RECORD = 36
    VT_INT_PTR = 37
    VT_UINT_PTR = 38
    VT_FILETIME = 64
    VT_BLOB = 65
    VT_STREAM = 66
    VT_STORAGE = 67
    VT_STREAMED_OBJECT = 68
    VT_STORED_OBJECT = 69
    VT_BLOB_OBJECT = 70
    VT_CF = 71
    VT_CLSID = 72
    VT_VERSIONED_STREAM = 73
    VT_BSTR_BLOB = 0x0FFF
    VT_VECTOR = 0x1000
    VT_ARRAY = 0x2000
    VT_BYREF = 0x4000
    VT_RESERVED = 0x8000
    VT_ILLEGAL = 0xFFFF
    VT_ILLEGALMASKED = 0x0FFF
    VT_TYPEMASK = 0x0FFF


class BCapConverter:
    BCAP_SOH = b"\x01"
    BCAP_EOT = b"\x04"

    _TIME_DIFFERENCE = 25569.0
    _SEC_ONEDAY = 24 * 60 * 60

    _DICT_TYPE_TO_VT = {
        int: (VarType.VT_I4, "i", False),
        float: (VarType.VT_R8, "d", False),
        datetime: (VarType.VT_DATE, "d", False),
        str: (VarType.VT_BSTR, "I%ds", False),
        bool: (VarType.VT_BOOL, "h", False),
        ctypes.c_bool: (VarType.VT_BOOL, "h", True),
        ctypes.c_ubyte: (VarType.VT_UI1, "B", True),
        ctypes.c_short: (VarType.VT_I2, "h", True),
        ctypes.c_ushort: (VarType.VT_UI2, "H", True),
        ctypes.c_int: (VarType.VT_I4, "i", True),
        ctypes.c_uint: (VarType.VT_UI4, "I", True),
        ctypes.c_long: (VarType.VT_I4, "l", True),
        ctypes.c_ulong: (VarType.VT_UI4, "L", True),
        ctypes.c_longlong: (VarType.VT_I8, "q", True),
        ctypes.c_ulonglong: (VarType.VT_UI8, "Q", True),
        ctypes.c_float: (VarType.VT_R4, "f", True),
        ctypes.c_double: (VarType.VT_R8, "d", True),
        ctypes.c_wchar_p: (VarType.VT_BSTR, "I%ds", True),
    }

    _DICT_VT_TO_TYPE = {
        VarType.VT_I2: ("h", 2),
        VarType.VT_I4: ("i", 4),
        VarType.VT_R4: ("f", 4),
        VarType.VT_R8: ("d", 8),
        VarType.VT_CY: ("q", 8),
        VarType.VT_DATE: ("d", 8),
        VarType.VT_BSTR: ("%ds", -1),
        VarType.VT_ERROR: ("i", 4),
        VarType.VT_BOOL: ("h", 2),
        VarType.VT_UI1: ("B", 1),
        VarType.VT_UI2: ("H", 2),
        VarType.VT_UI4: ("I", 4),
        VarType.VT_I8: ("q", 8),
        VarType.VT_UI8: ("Q", 8),
    }

    @staticmethod
    def datetime_to_vnt_date(datetime: datetime) -> float:
        return (
            datetime.timestamp() / BCapConverter._SEC_ONEDAY
            + BCapConverter._TIME_DIFFERENCE
        )

    @staticmethod
    def vnt_date_to_datetime(vnt_date: float) -> datetime:
        return datetime.fromtimestamp(
            (vnt_date - BCapConverter._TIME_DIFFERENCE) * BCapConverter._SEC_ONEDAY
        )

    @staticmethod
    def parse_endpoint(endpoint: str) -> Tuple[str, int]:

        parsed = urlsplit("//" + endpoint)
        host = ""
        port = 5007
        if parsed.hostname is None:
            raise ValueError("{} is invalid.".format(endpoint))

        host = parsed.hostname
        if parsed.port is not None:
            port = parsed.port

        return (host, port)

    def __init__(self, is_tcp: bool, should_return_hr: bool):
        self._is_tcp = is_tcp
        self._should_return_hr = should_return_hr
        self._is_comress = False
        self._compress_level = -1

    def set_compression_parameters(self, is_compress: bool, level=-1) -> None:
        self._is_comress = is_compress
        if level < -1 or level > 9:
            raise ValueError()

        self._compress_level = level

    def serialize(
        self, serial: int, version_or_retry: int, func_id: int, args: any
    ) -> bytes:

        stream = io.BytesIO()

        # b : Header - 1byte(signed char)
        stream.write(BCapConverter.BCAP_SOH)

        # < : Use little endian at b-CAP.
        # I : Message length(calculate later) - 4bytes(unsigned int)
        # H : Serial number - 2bytes(unsigned short)
        # h : Version(TCP) or retry(UDP) - 2bytes(short)
        stream.write(
            struct.pack(
                "<IHh",
                0,
                serial,
                version_or_retry,
            )
        )

        if self._is_comress and self._is_tcp:
            func_info_and_arg_stream = io.BytesIO()
            self._serialize_func_info_and_arg(func_info_and_arg_stream, func_id, args)
            uncompressed_data_length = func_info_and_arg_stream.tell()
            compressed_data = zlib.compress(
                func_info_and_arg_stream.getvalue(), self._compress_level
            )
            # I : Uncompressed data length - 4bytes(unsigned int)
            stream.write(struct.pack("<I", uncompressed_data_length))
            stream.write(compressed_data)
        else:
            self._serialize_func_info_and_arg(stream, func_id, args)

        if self._is_tcp:
            # b : Mode - 1byte(signed char)
            if self._is_comress is True:
                stream.write(b"\x01")
            else:
                stream.write(b"\x00")
        else:
            pass

        # b : Footer - 1byte(signed char)
        stream.write(BCapConverter.BCAP_EOT)

        packet_length = stream.tell()
        stream.seek(1)
        stream.write(struct.pack("<I", packet_length))

        return stream.getvalue()

    def _serialize_func_info_and_arg(
        self, stream: io.BytesIO, func_id: int, args: any
    ) -> None:

        # i : Function ID or Return code - 4bytes(int)
        # H : Number of Args - 2bytes(unsigned short)
        stream.write(
            struct.pack(
                "<iH",
                func_id,
                len(args),
            )
        )

        for arg in args:
            start_arg_pos = stream.tell()
            # Prepare an area to write the following data length (argument length)
            # 1. Data type
            # 2. The number of elements
            # 3. Data
            stream.write(b"\0\0\0\0")
            self._serialize_arg(stream, arg)
            end_arg_pos = stream.tell()
            # Write the length without the argument length
            stream.seek(start_arg_pos)
            stream.write(struct.pack("<I", end_arg_pos - start_arg_pos - 4))
            # Move to end
            stream.seek(0, 2)

    def _serialize_arg(self, stream: io.BytesIO, arg: any) -> None:

        if arg is None:
            stream.write(struct.pack("<HI", VarType.VT_EMPTY, 1))
        elif isinstance(arg, (list, tuple)):
            # Array(without bytes array)
            len_arg = len(arg)
            if len_arg == 0:
                stream.write(struct.pack("<HI", VarType.VT_EMPTY, 1))
            else:
                arg_type = type(arg[0])
                is_vnt_array = all(arg_type is type(x) for x in arg) is False

                if is_vnt_array:
                    # Variant array
                    stream.write(
                        struct.pack(
                            "<HI", VarType.VT_VARIANT | VarType.VT_ARRAY, len_arg
                        )
                    )
                    for e in arg:
                        self._serialize_arg(stream, e)
                elif arg_type in BCapConverter._DICT_TYPE_TO_VT:
                    (var_type, format_char, is_ctype) = BCapConverter._DICT_TYPE_TO_VT[
                        arg_type
                    ]
                    stream.write(
                        struct.pack("<HI", var_type | VarType.VT_ARRAY, len_arg)
                    )
                    for e in arg:
                        self._serialize_element(
                            stream, var_type, format_char, is_ctype, e
                        )
                else:
                    raise BCapException(
                        HResult.E_CAO_VARIANT_TYPE_NO_SUPPORT,
                        "Failed to serialize arguments.",
                    )
        elif isinstance(arg, (bytes, bytearray)):
            # Array(bytes array)
            len_arg = len(arg)
            stream.write(
                struct.pack(
                    "<HI%ds" % len_arg,
                    VarType.VT_ARRAY | VarType.VT_UI1,
                    len_arg,
                    arg,
                )
            )
        else:
            # Not array
            arg_type = type(arg)
            if arg_type in BCapConverter._DICT_TYPE_TO_VT:
                (var_type, format_char, is_ctype) = BCapConverter._DICT_TYPE_TO_VT[
                    arg_type
                ]
                stream.write(struct.pack("<HI", var_type, 1))
                self._serialize_element(stream, var_type, format_char, is_ctype, arg)
            else:
                raise BCapException(
                    HResult.E_CAO_VARIANT_TYPE_NO_SUPPORT,
                    "Failed to serialize arguments.",
                )

    def _serialize_element(
        self, stream: io.BytesIO, var_type: int, format_char: str, is_ctype: bool, value
    ) -> None:
        if var_type == VarType.VT_DATE:
            vnt_date = BCapConverter.datetime_to_vnt_date(value)
            stream.write(struct.pack("<" + format_char, vnt_date))
        elif var_type == VarType.VT_BSTR:
            if is_ctype:
                vnt_str = value.value.encode("utf-16le")
            else:
                vnt_str = value.encode("utf-16le")

            str_length = len(vnt_str)
            stream.write(
                struct.pack("<" + (format_char % str_length), str_length, vnt_str)
            )
        elif var_type == VarType.VT_BOOL:
            if value:
                stream.write(struct.pack("<" + format_char, -1))
            else:
                stream.write(struct.pack("<" + format_char, 0))
        else:
            if is_ctype:
                stream.write(struct.pack("<" + format_char, value.value))
            else:
                stream.write(struct.pack("<" + format_char, value))

    def deserialize(self, byte_array: bytes) -> Tuple[int, int, int, list]:

        # < : Use little endian at b-CAP.
        # b : Header - 1byte(signed char)
        # I : Message length(calculate later) - 4bytes(unsigned int)
        # H : Serial number - 2bytes(unsigned short)
        # H : Version(TCP) or retry(UDP) - 2bytes(unsigned short)
        format = "<bIHH"
        if self._is_tcp:
            mode = byte_array[-2]
            if len(byte_array) == 16:
                # %ds : Function information and arguments
                # b : Footer - 1byte(signed char)
                format += "%dsb" % (len(byte_array) - (1 + 4 + 2 + 2 + 1))
                (
                    soh,
                    message_length,
                    serial,
                    version_or_retry,
                    function_info_and_arg,
                    eot,
                ) = struct.unpack(format, byte_array)
            else:
                # %ds : Function information and arguments
                # b : Footer - 1byte(signed char)
                # b : Mode - 1byte(signed char)
                format += "%ds2b" % (len(byte_array) - (1 + 4 + 2 + 2 + 1 + 1))
                (
                    soh,
                    message_length,
                    serial,
                    version_or_retry,
                    function_info_and_arg,
                    mode,
                    eot,
                ) = struct.unpack(format, byte_array)

            if mode == 1:
                # _ is the length of uncompressed data. This is not used.
                _, compressed_data = struct.unpack(
                    "<I%ds" % (len(function_info_and_arg) - 4), function_info_and_arg
                )
                function_info_and_arg = zlib.decompress(compressed_data)
            else:
                pass
        else:
            # b : Footer - 1byte(signed char)
            format += "%dsb" % (len(byte_array) - (1 + 4 + 2 + 2 + 1))
            (
                soh,
                _,
                serial,
                version_or_retry,
                function_info_and_arg,
                eot,
            ) = struct.unpack(format, byte_array)

        # i : Return code - 4bytes(int)
        # H : Number of Args - 2bytes(unsigned short)
        format = "<iH%ds" % (len(function_info_and_arg) - (4 + 2))
        hr, number_of_args, args = struct.unpack(format, function_info_and_arg)

        deserialized_args = None
        if number_of_args > 0:
            stream = io.BytesIO(args)
            deserialized_args = []
            for i in range(number_of_args):
                # The length of argument data. This is not used.
                stream.seek(4, 1)
                deserialized_args.append(self._deserialize_args(stream))

        return (serial, version_or_retry, hr, deserialized_args)

    def _deserialize_args(self, stream: io.BytesIO) -> any:

        # H : Variant type - 2bytes(unsigned short)
        # I : The number of elements - 4bytes(unsigned int)
        var_type, number_of_elements = struct.unpack("<HI", stream.read(2 + 4))
        deserialized_args = None
        if (var_type & VarType.VT_ARRAY) != 0:
            # Array
            var_type = var_type ^ VarType.VT_ARRAY
            if var_type == VarType.VT_VARIANT:
                # Variant array
                deserialized_array = []
                for i in range(number_of_elements):
                    deserialized_array.append(self._deserialize_args(stream))
                deserialized_args = deserialized_array
            elif var_type == VarType.VT_UI1:
                # Bytes array
                (deserialized_args,) = struct.unpack(
                    "<%ds" % number_of_elements, stream.read(number_of_elements)
                )
            elif var_type in BCapConverter._DICT_VT_TO_TYPE:
                # Other array
                deserialized_array = []
                for i in range(number_of_elements):
                    deserialized_array.append(
                        self._deserialize_element(stream, var_type)
                    )
                deserialized_args = deserialized_array
            else:
                raise BCapException(
                    HResult.E_CAO_VARIANT_TYPE_NO_SUPPORT,
                    "Failed to deserialize arguments.",
                )
        else:
            # Not array
            if var_type in [VarType.VT_EMPTY, VarType.VT_NULL]:
                pass
            elif var_type in BCapConverter._DICT_VT_TO_TYPE:
                deserialized_args = self._deserialize_element(stream, var_type)
            else:
                raise BCapException(
                    HResult.E_CAO_VARIANT_TYPE_NO_SUPPORT,
                    "Failed to deserialize arguments.",
                )

        return deserialized_args

    def _deserialize_element(self, stream: io.BytesIO, var_type) -> any:

        format_char, value_length = BCapConverter._DICT_VT_TO_TYPE[var_type]
        deserialized_element = None
        if var_type == VarType.VT_BSTR:
            (str_length,) = struct.unpack("<I", stream.read(4))
            (str_buf,) = struct.unpack("<%ds" % str_length, stream.read(str_length))
            deserialized_element = str_buf.decode("utf-16le")
        else:
            (deserialized_element,) = struct.unpack(
                "<%s" % format_char, stream.read(value_length)
            )
            if var_type == VarType.VT_DATE:
                deserialized_element = BCapConverter.vnt_date_to_datetime(
                    deserialized_element
                )
            elif var_type == VarType.VT_BOOL:
                deserialized_element = deserialized_element != 0

        return deserialized_element

    def create_response_object(
        self, hr, deserialized_result
    ) -> Union[Tuple[int, any], any]:
        if self._should_return_hr:
            return (hr, deserialized_result)

        if hr < 0:
            raise BCapException(hr)

        return deserialized_result
