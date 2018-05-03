import logging
import socket

from tcp_client_server.proto import server as srv
from tcp_client_server.contexts import stream_socket_control
from tcp_client_server.logging import LOG_CONF

logging.basicConfig(**LOG_CONF)


def server():
    sock_init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with stream_socket_control(sock_init,
                               mode='server',
                               fatal_errors_verbosity=True) as listener:
        while True:
            logging.info(f'Started accepting requests at {listener.getsockname()[0]}:{listener.getsockname()[1]}.')
            conn, addr = listener.accept()
            logging.info(f'Serving client {addr[0]}:{addr[1]}.')
            srv.serve_requests(conn)

            conn.close()
            logging.info(f'Client {addr[0]}:{addr[1]} closed connection.')


if __name__ == '__main__':
    server()
