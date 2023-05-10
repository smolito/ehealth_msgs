import os
import matplotlib.pyplot as plot
import scouting
import socket
import json
import random
import datetime

client_root = "_client_creations"

standard = "hl7"
send_whole_file = False
plot_bool = True
t_from = "20110614165355"
t_to = "20110614192413"
patient = "12062011"
vital_p = ["001000^VITAL HR", "014000^VITAL TRECT"]
parameter_list = scouting.unique_vitals_in_msgs

if not os.path.exists(client_root):
    os.makedirs(client_root)


def datetime_from_msg(msg_time):
    d = datetime.datetime(int(msg_time[0:4]), int(msg_time[4:6]), int(msg_time[6:8]))
    t = datetime.time(int(msg_time[8:10]), int(msg_time[10:12]), int(msg_time[12:14]))
    combined = d.combine(d, t)

    return combined


def plot_vitals(time_at_observation, vital_values, pid, vital_parameter, units):
    # print("last times are: ", time_at_observation[-5:])
    # print("last vitals are: " + str(vital_values[-5:]))

    observation_times = []

    for time in time_at_observation:
        observation_times.append(datetime_from_msg(time))

    if not os.path.exists(os.path.join(client_root, "_plots")):
        os.makedirs(os.path.join(client_root, "_plots"))

    plot.plot(observation_times, vital_values)
    plot.xlabel("time")
    plot.ylabel(units)
    plot.title("patient " + pid + " " + vital_parameter)
    plot.savefig(os.path.join(client_root, "_plots", pid + "_" + vital_parameter + ".png"))
    plot.show()


def request(form, whole_file, bool_plot, pid, vital_parameter, time_from, time_to):
    host = "127.0.0.1"
    port = 9090

    req_init = {
        "form": "",
        "whole_file": whole_file,
        "plot": bool_plot,
        "pid": pid,
        "vital_parameter": vital_parameter,
        "time_from": time_from,
        "time_to": time_to,
        "msg_id": random.randint(0, 10000)
    }

    if form.strip() == "hl7":
        req_init["form"] = "hl7"
        if not os.path.exists(os.path.join(client_root, "_hl7_msgs")):
            os.makedirs(os.path.join(client_root, "_hl7_msgs"))
    elif form.strip() == "fhir":
        req_init["form"] = "fhir"
        if not os.path.exists(os.path.join(client_root, "_fhir_msgs")):
            os.makedirs(os.path.join(client_root, "_fhir_msgs"))
    else:
        print("not a valid standard, sending hl7 request")
        req_init["form"] = "hl7"

    req = json.dumps(req_init)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("looking for id confirmation:", req_init["msg_id"])
    client_socket.send(str(req_init["msg_id"]).encode())
    request_confirmation = client_socket.recv(1024).decode()
    print("got", request_confirmation)
    if not int(request_confirmation) == req_init["msg_id"]:
        print("server didn't respond with msg_id confirmation")
    else:
        msg_id = request_confirmation

    client_socket.send(req.encode())

    # shortcut of a buffer size to easily fit even the biggest whole file; not exactly the best solution!
    response_data = client_socket.recv(4194304).decode()
    response_data = json.loads(response_data)

    if plot_bool:
        plot_data = client_socket.recv(16384).decode()
        plot_data = json.loads(plot_data)
    else:
        plot_data = ""

    if msg_id != "" and response_data:
        client_socket.send("response received".encode())

    """
    print(plot_data[0])
    print(type(plot_data[0]), len(plot_data[0]))
    print(plot_data[1])
    print(type(plot_data[1]), len(plot_data[1]))
    print(plot_data[2])
    print(type(plot_data[2]))
    print(plot_data[3])
    print(type(plot_data[3]))
    print(plot_data[4])
    print(type(plot_data[4]))
    """

    client_socket.close()
    return response_data, plot_data, msg_id


response, data2plot, msgid = request(
    standard,
    send_whole_file,
    plot_bool,
    patient,
    vital_p,
    t_from,
    t_to
)


def reaction2response(data_from_request):

    if standard == "hl7":
        with open(os.path.join(client_root, "_hl7_msgs", patient + "_" + msgid + ".txt"), "w") as write_file:
            write_file.writelines(data_from_request)
            write_file.close()

    if standard == "fhir":
        with open(os.path.join(client_root, "_fhir_msgs", patient + "_" + msgid + ".txt"), "w") as write_file:
            write_file.writelines(data_from_request)
            write_file.close()


# plot_vitals(data2plot[0], data2plot[1], data2plot[2], data2plot[3], data2plot[4])
reaction2response(response)
for vital in data2plot:
    plot_vitals(vital[0], vital[1], vital[2], vital[3], vital[4])

