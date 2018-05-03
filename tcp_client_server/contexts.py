import socket
import logging
import traceback

from contextlib import contextmanager

from .utils import ask_endpoint


@contextmanager
def stream_socket_control(sock,
                          mode,
                          server_conns_num=3,
                          fatal_errors_verbosity=False,
                          socket_opts=None):
    try:
        if socket_opts is None:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            for opt in socket_opts:
                sock.setsockopt(*opt)
 
        print('Enter address of current endpoint: ')
        cur_endpoint = ask_endpoint()
        sock.bind(cur_endpoint)
    
        if mode == 'client':
            print('Enter target address: ')
            address = ask_endpoint()
            sock.connect_ex(address)

        elif mode == 'server':
            sock.listen(conns_num)

        else:
            raise WrongModeError(f'Unknown mode {mode}.')

        yield sock
    
    except (KeyboardInterrupt, EOFError) as quit_cmd:
        logging.info(f'Shutting down {mode}...')

    except Exception as fatal_error:
        if not fatal_errors_verbosity:
            logging.critical(f'Fatal error ({type(fatal_error)}): {fatal_error.message}')
        else:
            logging.critical(traceback.format_exc())

    finally:
        sock.close()
        logging.info(f'Successfully stopped.')

