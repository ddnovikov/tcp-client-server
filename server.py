import logging
import socket
import sys

from tcp_client_server import proto
from tcp_client_server.contexts import stream_socket_control


def server():
    logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', stream=sys.stdout)
    sock_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with stream_socket_control(sock_init, 
                                   mode='server', 
                                   fatal_errors_verbosity=True) as listener:
            while True:
                conn, addr = listener.accept()
                logging.info(f'Serving client from {addr[0]}:{addr[1]}.')
                serve_requests(conn)
        
                conn.close()
                logging.info(f'Client {addr[0]}:{addr[1]} closed connection.')
        
            listener.close()


if __name__ == '__main__':
    server()

