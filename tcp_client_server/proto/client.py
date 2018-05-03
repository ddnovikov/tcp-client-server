import socket

from ctypes import *

from . import shared
from .. import tcp, processing


def send_request(channel, msgs):
    for msg in msgs:
        tcp.send(channel, msg)


def download(channel, path):
    length = c_uint32(socket.htonl(sizeof(shared.TYPE_GET) + len(path)))

    send_request(channel, [length, shared.TYPE_GET, path.encode()])
    length, response_type = shared.receive_headers(channel, sizeof(length), sizeof(TYPE_GET))
    
    if response_type == shared.TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == shared.TYPE_GET:
        return processing.process_get_response(channel, path, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type)


def list_files(channel):
    length = c_uint32(socket.htonl(1))

    send_request(channel, [length, shared.TYPE_LIST])
    length, response_type = shared.receive_headers(channel, sizeof(length), sizeof(shared.TYPE_LIST))
 
    if response_type == shared.TYPE_ERROR:
        return processing.process_error_response(channel, length)
    elif response_type == shared.TYPE_LIST:
        return processing.process_list_response(channel, length)
    else:
        return processing.process_unexpected_response(channel, length, response_type) 

