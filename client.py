import logging
import socket
import sys

from tcp_client_server.proto import client as clnt
from tcp_client_server.contexts import stream_socket_control


def client():
    logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', stream=sys.stdout)
    sock_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with stream_socket_control(sock_init, 
                               mode='client', 
                               fatal_errors_verbosity=True) as sock:
        while True:
            print('>>> ', end='')
            command = input()
            command = command.strip().split()
    
            if command[0] == '/quit':                
                break

            elif command[0] == '/get' and command[1]:
                res = clnt.download(sock, command[1])
                if not res:
                    logging.info(f'Couldn\'t download file {command[1]}.')

            elif command[0] == '/list':
                clnt.list_files(sock)

            else:
                print(f'Unknown command {command}. Supported commands: /get <path_to_file>; /quit')
    
        sock.close()
    

if __name__ == '__main__':
    client()

