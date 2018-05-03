import os
import socket

from ctypes import c_uint32, sizeof

from . import shared
from .. import tcp
from ..processing import process_unexpected_message
from ..utils import read_file_as_bytes


def serve_requests(channel):
    while serve_request(channel):
        pass


def send_error(channel, error_msg):
    length = c_uint32(socket.htonl(sizeof(shared.TYPE_ERROR) + len(error_msg)))
    shared.send_headers(channel, [length, shared.TYPE_ERROR, error_msg.encode()])

    return True


def serve_file(channel, path_length):
    path = str(tcp.receive_msg(channel, path_length, bufsize=None))
    file_size = os.path.getsize(path)

    length = c_uint32(socket.htonl(sizeof(shared.TYPE_GET) + file_size))
    shared.send_headers(channel, [length, shared.TYPE_GET])

    for chunk in read_file_as_bytes(path, chunksize=4096):
        tcp.send(channel, chunk)

    return True


def serve_list(channel):
    pass


def serve_request(channel):
    length, response_type = shared.receive_headers(channel, 4, 1)

    if length > shared.MAX_MESSAGE_LENGTH:
        send_error(channel, f'Error: recieved message that is longer ({length} bytes) than '
                            f'MAX_MESSAGE_LENGTH ({shared.MAX_MESSAGE_LENGTH} bytes).')

    if response_type == shared.TYPE_GET:
        return serve_file(channel, length - 1)
    elif response_type == shared.TYPE_LIST:
        return serve_list(channel)
    else:
        return process_unexpected_message(channel, length, response_type)
