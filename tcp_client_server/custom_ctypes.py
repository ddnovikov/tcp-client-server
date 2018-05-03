import ctypes


class c_uint32_(ctypes.c_uint32):
    def __invert__(self):
        return ctypes.c_uint32(~self.value)

    def __or__(self, other):
        return ctypes.c_uint32(self.value | other.value)

    def __and__(self, other):
        return ctypes.c_uint32(self.value & other.value)

    def __xor__(self, other):
        return ctypes.c_uint32(self.value ^ other.value)


class c_uint8_(ctypes.c_uint8):
    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

