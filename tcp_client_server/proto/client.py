import socket

from ctypes import *

from . import shared
from .. import processing


def download(channel, path):
    length = c_uint32(socket.htonl(sizeof(shared.TYPE_GET) + len(path)))

    shared.send_headers(channel, [length, shared.TYPE_GET, path.encode()])
    length, response_type = shared.receive_headers(channel, sizeof(length), sizeof(shared.TYPE_GET))
    
    if response_type == shared.TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == shared.TYPE_GET:
        return processing.process_get_response(channel, path, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type)


def list_files(channel):
    length = c_uint32(socket.htonl(1))

    shared.send_headers(channel, [length, shared.TYPE_LIST])
    length, response_type = shared.receive_headers(channel, sizeof(length), sizeof(shared.TYPE_LIST))
 
    if response_type == shared.TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == shared.TYPE_LIST:
        return processing.process_list_response(channel, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type)
