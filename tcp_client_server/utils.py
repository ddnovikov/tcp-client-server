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


def read_file_as_bytes(filename, chunksize=4096):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
            else:
                break
