"""
name: Bar Assulin
date: 20/10/24
server of md5
"""


import socket
import protocol
from threading import Thread
from threading import Lock


QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
STR = '25d55ad283aa400af464c76d713c07ad'
global CURRENT
CURRENT = 0
JUMPS = 100000
MAX_NUMBER = 99999999
global found, found_num
found = False
found_num = None
lock = Lock()


def handle_connection(client_socket, client_address):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    global found, found_num, CURRENT
    global lock
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        # handle the communication
        cores = client_socket.recv(1).decode()
        if cores == "":
            cores = None
        else:
            cores = protocol.recv_protocol(client_socket, cores)
            if cores.isnumeric():
                cores = int(cores)
            print("cores")
            print(cores)
            while not found:
                lock.acquire()
                client_socket.send(protocol.send_protocol(f"{CURRENT}/{JUMPS}/{STR}".encode()))
                CURRENT = CURRENT + JUMPS*cores
                print(CURRENT)
                print("CURRENT")
                lock.release()
                print("got here first")
                data = client_socket.recv(1).decode()
                print("got here first2")

                if data == "":
                    data = None
                    print("none")
                else:
                    print("yes")
                    data = protocol.recv_protocol(client_socket, data)
                    print("goy here")
                    print(data)
                    data2 = data.split("/", 1)
                    print(data2[0])
                    if data2[0] == "True":
                        print("true")
                        found = True
                        found_num = int(data.split("/", 1)[1])

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


def main():
    global found
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(10)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        while not found:
            try:
                client_socket, client_address = server_socket.accept()
                print("worked")
                thread = Thread(target=handle_connection,
                                args=(client_socket, client_address))
                thread.start()
            except socket.timeout:
                print("Timeout! No connection within 10 seconds.")

        print("done")
        print(found_num)
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
