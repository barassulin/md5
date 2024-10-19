"""
name: Bar Assulin
date: 20/10/24
client of md5
"""

import socket
import protocol
from threading import Thread
import hashlib
import os


SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
global found, stringi, found_number
stringi = ''
found = False
found_number = 0


def get_md5_of_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def handle_connection(start_number, end_number):
    """
    handle a connection
    :param start_number: the starting number
    :param end_number: the ending number
    :return: None
    """
    global found, found_number

    x = start_number
    while x != end_number and found is not True:
        stringdi = get_md5_of_string(str(x))
        if stringdi == stringi:
            found_number = x
            found = True
        x = x+1


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.settimeout(20)
        # send how many cores
        cores = os.cpu_count()
        client_socket.send(protocol.send_protocol(cores))        # recv start and jumps
        data = client_socket.recv(1).decode()
        print("rec")
        if data == "":
            data = None
        else:
            data = protocol.recv_protocol(client_socket, data)
            print(data)
            print("data")
            data2 = data.split('/', 2)
            start_number = data2[0]
            if start_number.isnumeric():
                start_number = int(start_number)
            print("data2")
            print(data2)
            jump = data2[1]
            if jump.isnumeric():
                jump = int(jump)
            global stringi
            stringi = data2[2]
            end = start_number + jump * cores
            end_number = start_number + jump
            "thread"
            while not found and start_number != end:
                thread = Thread(target=handle_connection,
                                args=(start_number, end_number))
                thread.start()
                stat_number = end_number
                end_number = end_number+jump
            client_socket.send(protocol.send_protocol(f"{found}/{found_number}".encode()))
            print("sent")

    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
