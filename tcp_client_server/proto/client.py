import socket

from ctypes import *

from . import tcp, processing
from .custom_ctypes import c_uint8_
from .utils import hex_dump

c_uint8 = c_uint8_

TYPE_GET = c_uint8(0x00)
TYPE_LIST = c_uint8(0x01)
TYPE_ERROR = c_uint8(0xff)


def send_request(channel, msgs):
    for msg in msgs:
        tcp.send(channel, msg)


def receive_headers(channel, 
                    length_size, 
                    request_type_size):
    length = tcp.receive_msg(channel, length_size, bufsize=None)

    response_type = tcp.receive_msg(channel, request_type_size, bufsize=None)
    response_type = c_uint8(int.from_bytes(response_type, byteorder='big'))

    length = int.from_bytes(length, byteorder='big') - 1

    return length, response_type


def download(channel, path):
    length = c_uint32(socket.htonl(sizeof(TYPE_GET) + len(path)))

    send_request(channel, [length, TYPE_GET, path.encode()])
    length, response_type = receive_headers(channel, sizeof(length), sizeof(TYPE_GET))
    
    if response_type == TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == TYPE_GET:
        return processing.process_get_response(channel, path, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type)


def list_files(channel):
    length = c_uint32(socket.htonl(1))

    send_request(channel, [length, TYPE_LIST])
    length, response_type = receive_headers(channel, sizeof(length), sizeof(TYPE_LIST))
 
    if response_type == TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == TYPE_LIST:
        return processing.process_list_response(channel, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type) 
 
