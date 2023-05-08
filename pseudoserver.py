import json
import os
import socket


def vitals2plot(pid, vital_parameter, time_from, time_to):
    vital_values = []
    time_at_observation = []
    units_measure = ""

    if not int(time_from) < int(time_to):
        return print("can't plot vital graph, incorrect time input")

    with open(os.path.join("_data_by_pid", pid + ".txt"), "r") as read_file:

        for line in read_file:
            segment = line.split("|")

            if segment[0] == "OBR" and int(time_from) <= int(segment[7]) <= int(time_to):
                one_block_check = True

            if segment[0] == "OBX" and segment[3] == vital_parameter and one_block_check:
                vital_values.append(int(segment[5]))
                time_at_observation.append(segment[14])
                units_measure = segment[6]
                one_block_check = False

    read_file.close()
    return time_at_observation, vital_values, pid, vital_parameter, units_measure


def simple_comm():
    host = "127.0.0.1"
    port = 9090

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    socket_connection, address = server_socket.accept()
    print("got a connection from: " + str(address))

    while True:
        request = socket_connection.recv(1024)

        if request.decode() == "response received":
            break

        request = request.decode()
        request = json.loads(request)
        print(request)

        if request["whole_file"]:
            file = open(os.path.join("_data_by_pid", request["pid"] + ".txt"), "r")
            response = file.read().encode()
            file.close()
            socket_connection.sendall(response)

        if request["plot"]:
            plot_data = vitals2plot(
                request["pid"],
                request["vital_parameter"],
                request["time_from"],
                request["time_to"]
            )
            print(type(plot_data))
            response = json.dumps(plot_data).encode()
            print(response.__sizeof__())
            socket_connection.sendall(response)

    server_socket.close()


simple_comm()
