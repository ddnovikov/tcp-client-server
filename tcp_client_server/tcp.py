def send(channel, data):
    channel.send(data)


def receive_chunks(channel, size, bufsize=4096):
    recieved_bytes_cnt = 0

    while recieved_bytes_cnt < size:
        if bufsize is None:
            result = channel.recv(size-recieved_bytes_cnt)
        else:
            result = channel.recv(bufsize)

        if result is None:
            raise StopIteration
        recieved_bytes_cnt += len(result)

        yield result


def receive_msg(channel, size, bufsize=4096):
    recieved_bytes = b''

    for chunk in receive_chunks(channel, size, bufsize):
        recieved_bytes += chunk

    return recieved_bytes

