def hex_dump(bytes_, count, verbose=False):
    if verbose:
        print(f'Dumping {count} bytes.')

    for i in bytes_[:count]:
        print(hex(i), end=' ')

    print()


def ask_endpoint():
    print('Host: ', end='')
    host = input()

    print('Port: ', end='')
    port = int(input())

    return host, port

