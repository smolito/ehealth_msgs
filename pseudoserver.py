import json
import os
import socket
import datetime


def create_hl7(pid, vital_parameter, send_whole_file, time_from, time_to):
    whole_msg = []
    msgid = 1
    obx = ""
    obx_num = 1
    observation_time = time_from

    with open(os.path.join("_data_by_pid", pid + ".txt"), "r") as read_patient_file:

        for readline in read_patient_file:
            segment = readline.split("|")

            if segment[0] == "OBR" and int(time_from) <= int(segment[7]) <= int(time_to):
                observation_time = segment[7]

            if segment[0] == "OBX" and send_whole_file:
                obx = obx + readline

            if segment[0] == "OBX":
                if int(time_from) <= int(observation_time) <= int(time_to) and vital_parameter.__contains__(segment[3].strip()):
                    obx_init = "OBX|" + str(obx_num) + "|NM|" + segment[3].strip() + "|" + segment[4] + "|" + segment[
                        5] + "|" + segment[6] + "|||||" + segment[11] + "|||" + segment[14] + "|||" + "\n"
                    obx = obx + obx_init
                    obx_num += 1

            if segment[0] == "MSA" and obx != "":
                msh_header = "MSH|^~\&|" + "pseudoserver|" + "userpc|" + "client|" + "client facility|" + datetime.datetime.now().strftime(
                    "%Y%m%d%H%M%S") + "|ORU^R01^ORU_R01|" + str(
                    msgid) + "|T|" + "|2.5|" + "||" + "NE|" + "AL|" + "CZE|" + "ASCII|" + "||ASCII" + "\n"
                pid_segment = "PID|||" + pid + "||^^^^^^L^A|||O" + "\n"
                orc = "ORC|RE" + "\n"
                obr = "OBR|1|||VITAL|||" + observation_time + "||||||||||||||||||A" + "\n"
                msh_tail = "MSH|^~\&|||||||ACK^R01^ACK|" + str(msgid) + "|P|||||||ASCII||ASCII" + "\n"
                msa = "MSA|AA|" + str(msgid) + "\n"
                msg_block = msh_header + pid_segment + orc + obr + obx + msh_tail + msa + "\n"
                whole_msg.append(msg_block)
                msgid += 1
                obx = ""
                obx_num = 1
    read_patient_file.close()
    # with open("_test.txt", "w") as write:
    #     write.writelines(whole_msg)
    return whole_msg


# creates fhir message, not in json
def create_fhir(request_data):
    whole_message = []
    msg_id = 1
    pid = request_data["subject"]
    vitals = request_data["code"]
    vital_values = []
    status = "partial"
    time_from = request_data["effective"][0]
    time_to = request_data["effective"][1]
    issued = request_data["issued"]
    one_block_check = False

    with open(os.path.join("_data_by_pid", pid + ".txt"), "r") as read_file:
        for readline in read_file:
            segment = readline.split("|")
            # print(readline)
            if segment[0] == "OBR" and int(time_from) <= int(segment[7]) <= int(time_to):
                one_block_check = True

            if segment[0] == "OBX" and vitals.__contains__(segment[3].strip()) and one_block_check:
                effective_date_time = segment[14]
                value_quantity_one_vital = {
                    "value": float(segment[5]),
                    "unit": segment[6],
                    "code": segment[3].strip()
                }
                vital_values.append(value_quantity_one_vital)

            if segment[0] == "MSA" and vital_values != []:
                one_block_check = False
                observation_message_block = {"resourceType": "Observation", "identifier": msg_id, "subject": pid,
                                             "status": status, "effectiveDateTime": effective_date_time,
                                             "issued": issued, "valueQuantity": vital_values}
                whole_message.append(observation_message_block)
                msg_id += 1
                vital_values = []

    return whole_message


def vitals2plot(pid, vital_parameter, time_from, time_to):
    vital_values = []
    time_at_observation = []
    units_measured = ""
    one_block_check = False

    if not int(time_from) < int(time_to):
        return print("can't plot vital graph, incorrect time input")

    with open(os.path.join("_data_by_pid", pid + ".txt"), "r") as read_file:
        for line in read_file:
            segment = line.split("|")

            if segment[0].strip() == "OBR" and int(time_from) <= int(segment[7]) <= int(time_to):
                one_block_check = True

            if one_block_check:
                if segment[0] == "OBX" and segment[3].strip() == vital_parameter:
                    vital_values.append(float(segment[5]))
                    time_at_observation.append(segment[14])
                    units_measured = segment[6]
                    one_block_check = False

    read_file.close()
    return time_at_observation, vital_values, pid, vital_parameter, units_measured


def simple_comm():
    host = "127.0.0.1"
    port = 9090

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    socket_connection, address = server_socket.accept()
    print("got a connection from: " + str(address))

    while True:
        initial_request = socket_connection.recv(1024).decode()
        initial_request = json.loads(initial_request)
        message_id = initial_request[0]
        form = initial_request[1]
        plot = initial_request[2]
        print("initial request: ", initial_request, initial_request.__sizeof__(), "bytes")
        # print(message_id, type(message_id), form, type(form))
        socket_connection.send(message_id.encode())

        request = socket_connection.recv(1024)

        request = request.decode()
        request = json.loads(request)

        if form == "fhir":
            response = create_fhir(
                request
            )
            response = json.dumps(response).encode()
            socket_connection.sendall(response)

        if form == "hl7":
            response = create_hl7(
                request["pid"],
                request["vital_parameter"],
                request["whole_file"],
                request["time_from"],
                request["time_to"]
            )
            response = json.dumps(response).encode()
            socket_connection.sendall(response)

        if plot:
            if form == "hl7":
                plot_data = []
                for vital in request["vital_parameter"]:
                    plot_data.append(vitals2plot(
                        request["pid"],
                        vital,
                        request["time_from"],
                        request["time_to"]
                    ))
                # print(type(plot_data))
                response = json.dumps(plot_data).encode()
                # print(response.__sizeof__())
                socket_connection.sendall(response)
            elif form == "fhir":
                plot_data = []
                print(request["subject"], type(request["subject"]))
                print(request["code"])
                print(request["effective"][0])
                print(request["effective"][1])
                for vital in request["code"]:
                    plot_data.append(vitals2plot(
                        str(request["subject"]),
                        vital,
                        request["effective"][0],
                        request["effective"][1]
                    ))
                response = json.dumps(plot_data).encode()
                socket_connection.sendall(response)

        if socket_connection.recv(1024).decode() == "response received":
            break

    server_socket.close()


# create_hl7("12062011", ["001000^VITAL HR", "014000^VITAL TRECT"], False, "20110614165355", "20110614192413")
simple_comm()
