from ctypes import *

from . import shared


def serve_requests(channel):
    while serve_request(channel):
        pass


def send_error(channel, error):
    pass


def serve_file(channel, path_length):
    pass


def serve_list(channel):
    pass


def process_unexpected_message(channel, length, request_type):
    pass


def serve_request(channel):
    length, response_type = shared.receive_headers(channel, 4, 1)

    if response_type == shared.TYPE_GET:
        return serve_file(channel, length - 1)
    elif response_type == shared.TYPE_LIST:
        return serve_list(client)
    else:
        return process_unexpected_message(client, length, response_type)

