import os
import socket

from ctypes import c_uint32, c_uint8, sizeof

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
    path = tcp.receive_msg(channel, path_length + 1, bufsize=None).decode()
    file_size = os.path.getsize(path)

    length = c_uint32(socket.htonl(sizeof(shared.TYPE_GET) + file_size))
    shared.send_headers(channel, [length, shared.TYPE_GET])

    for chunk in read_file_as_bytes(path, chunksize=4096):
        tcp.send(channel, chunk)

    return True


def serve_list(channel):
    files_list = list(filter(lambda f: os.path.isfile(f)
                                  and not f.startswith('.'),
                             os.listdir('.')))

    if not files_list:
        send_error(channel, f'Error: unable to count files.')

    msg_size = sizeof(shared.TYPE_LIST) + len(files_list) + sum([len(fn) for fn in files_list])
    length = c_uint32(socket.htonl(msg_size))

    msg = [length, shared.TYPE_LIST]
    for fn in files_list:
        msg += [c_uint8(socket.htonl(len(fn))), fn.encode()]

    shared.send_headers(channel, msg)

    return True


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
