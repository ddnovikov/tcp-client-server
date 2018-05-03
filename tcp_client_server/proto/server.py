import socket

from ctypes import *

from . import shared


def serve_requests(channel):
    while serve_request(channel):
        pass


def send_error(channel, error_msg):
    length = c_uint32(socket.htonl(sizeof(shared.TYPE_ERROR) + len(error_msg)))
    shared.send_headers(channel, [length, shared.TYPE_ERROR, error_msg.encode()])


def serve_file(channel, path_length):
    pass


def serve_list(channel):
    pass


def process_unexpected_message(channel, length, request_type):
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
