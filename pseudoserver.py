import json
import os
import socket


def simple_comm():
    host = "127.0.0.1"
    port = 9090

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    socket_connection, address = server_socket.accept()
    print("got a connection from: " + str(address))

    while True:
        data = socket_connection.recv(1024)
        response = "server response"
        socket_connection.sendall(response.encode())


simple_comm()


def server_program():
    host = "127.0.0.1"
    port = 9090

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get a socket instance
    server_socket.bind((host, port))  # bind() takes TUPLE as an argument

    server_socket.listen()  # how many connections until it starts rejecting new ones
    socket_connection, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than .recv bytes
        data_received = socket_connection.recv(1024).decode()

        if not data_received:
            print("no data received")
            break

        print("size: " + str(data_received.__sizeof__()) + " bytes," + " msg: " + str(data_received))

        data_to_send = json.loads(data_received)
        print(type(data_to_send), data_to_send)

        if data_to_send[0]:  # if a whole file is requested
            response = "_data_by_pid/" + str(data_to_send[1]) + ".txt"
            file_size = os.path.getsize(response)
            socket_connection.send(("sending " + data_to_send[1] + " size " + str(file_size)).encode())

            file = open(response, "rb")
            data_response = file.read()
            socket_connection.sendall(data_response)
            file.close()

        # socket_connection.send(data_to_send.encode())  # send data to the client
