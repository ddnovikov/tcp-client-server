import logging
import os
import re

from . import tcp
from .utils import hex_dump
from .logging import LOG_CONF

logging.basicConfig(**LOG_CONF)


def process_error_response(channel, text_size):
    error_msg = tcp.receive_msg(channel, text_size, bufsize=None)
    logging.error(f'Server error: {error_msg}')


def process_unexpected_message(channel, length, msg_type):
    logging.error(f'Protocol error: unexpected message (type={msg_type}, length={length}).')
    data = tcp.receive_msg(channel, length, bufsize=None)
    logging.error(f'Payload dump: {hex_dump(data, len(data))}.')


def process_get_response(channel, path, file_size):
    path = 'downloads/' + os.path.basename(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    logging.info(f'Downloading {file_size} bytes...')
    
    with open(path, 'wb') as f:
        for chunk in tcp.receive_chunks(channel, file_size):
            f.write(chunk)

    logging.info('Successfully downloaded.')


def process_list_response(channel, length):
    res = tcp.receive_msg(channel, length, bufsize=None)
    res = re.sub(b'[\x00-\x10]', b' ', res)[1:]
    res = res.decode().split()
   
    print('List of available files:') 
    for filename in res:
        print(f'    {filename}')

