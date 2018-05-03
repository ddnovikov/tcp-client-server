def send(channel, address, message):
    message = bytes(message.encode('utf-8'))
    sock.sendto(message, address)


def recieve(channel):
    data, addr_in = sock.recvfrom(1536)
    data = data.decode('utf-8')

    return data

