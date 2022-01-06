from ctypes import c_int32


class HResult:
    E_FAIL = c_int32(0x80004005).value
    E_CAO_VARIANT_TYPE_NO_SUPPORT = c_int32(0x80000203).value
    S_EXECUTING = c_int32(0x00000900).value
    E_INVALID_PACKET = c_int32(0x80010000).value


class BCapException(Exception):
    def __init__(self, hr: int, message: str = None):
        self.hr = hr
        if type(message) is str:
            super().__init__("[{0:#010X}] {1}".format(hr & 0xFFFFFFFF, message))
        else:
            super().__init__(
                "[{:#010X}] b-CAP server returns an error.".format(hr & 0xFFFFFFFF)
            )
