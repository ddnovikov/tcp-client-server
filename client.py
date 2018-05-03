import logging
import socket

from tcp_client_server.proto import client as clnt
from tcp_client_server.contexts import stream_socket_control
from tcp_client_server.logging import LOG_CONF

logging.basicConfig(**LOG_CONF)


def client():
    sock_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with stream_socket_control(sock_init, 
                               mode='client', 
                               fatal_errors_verbosity=True) as sock:
        logging.info(f'Connection to server established.')
        while True:
            print('>>> ', end='')
            command = input()
            command = command.strip().split()
    
            if command[0] == '/quit':
                raise EOFError

            elif command[0] == '/get' and command[1]:
                res = clnt.download(sock, command[1])

            elif command[0] == '/list':
                clnt.list_files(sock)

            else:
                print(f'Unknown command {command}. Supported commands: /get <path_to_file>; /quit')
    

if __name__ == '__main__':
    client()
