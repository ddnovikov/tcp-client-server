from .. import tcp
from ..custom_ctypes import c_uint8_

c_uint8 = c_uint8_

TYPE_GET = c_uint8(0x00)
TYPE_LIST = c_uint8(0x01)
TYPE_ERROR = c_uint8(0xff)


def receive_headers(channel, 
                    length_size, 
                    request_type_size):
    length = tcp.receive_msg(channel, length_size, bufsize=None)

    response_type = tcp.receive_msg(channel, request_type_size, bufsize=None)
    response_type = c_uint8(int.from_bytes(response_type, byteorder='big'))

    length = int.from_bytes(length, byteorder='big') - 1

    return length, response_type

