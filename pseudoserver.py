import os
import socket


def server_program():
    host = "127.0.0.1"
    port = 3001

    server_socket = socket.socket()  # get a socket instance
    # bind() takes TUPLE as an argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than .recv bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("size: " + str(data.__sizeof__()) + " bytes" + " from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()


server_program()
