"""
Author: Bar Assulin
Date: 20.10.24
Description: server.py for md5
"""
END_SIGN = "!"


def send_protocol(message):
    """
    send a string with her length
    :param message: the string
    :return: a string with her length
    """
    try:
        length = str(len(message))
    except Exception:
        message = str(message)
        length = str(len(message))
        message = message.encode()

    message = length.encode() + END_SIGN.encode() + message
    print("sending - protocol")
    print(message)

    return message


def recv_protocol(socket, message):
    """
    get from socket the length of the string and the string
    :param socket: the socket,
    :param message: the message
    :return: the string
    """
    message_length = len(END_SIGN.encode())
    message = message + socket.recv(message_length - len(message)).decode()
    while END_SIGN not in message:
        message = message + socket.recv(1).decode()
    length = int(message[:-message_length])
    message = socket.recv(1)
    while len(message) < length:
        message = message + socket.recv(1)
    print("reciving - protocol")
    print(message)
    try:
        message = message.decode()
    except Exception:
        pass
    return message
