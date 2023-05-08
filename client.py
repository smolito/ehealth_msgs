import os
import matplotlib.pyplot as plot
import scouting
import socket
import json
import datetime

client_root = "_client_creations"

send_whole_file = True
plot_bool = True
t_from = "20110622092400"
t_to = "20110622095000"
patient = "2011024"
vital_p = "001000^VITAL HR"
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

    if whole_file:
        if not os.path.exists(os.path.join(client_root, "whole_files")):
            os.makedirs(os.path.join(client_root, "whole_files"))

    req_init = {
        "form": "",
        "whole_file": whole_file,
        "plot": bool_plot,
        "pid": pid,
        "vital_parameter": vital_parameter,
        "time_from": time_from,
        "time_to": time_to
    }

    if form.strip() == "hl7":
        req_init["form"] = "hl7"
    elif form.strip() == "fhir":
        req_init["form"] = "fhir"
    else:
        print("not a valid standard sending hl7 request")
        req_init["form"] = "hl7"

    req = json.dumps(req_init)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(req.encode())

    # shortcut of a buffer size to easily fit even the biggest whole file; not exactly the best solution!
    response_data = client_socket.recv(4194304).decode()
    plot_data = client_socket.recv(4096).decode()

    plot_data = json.loads(plot_data)
    client_socket.send("response received".encode())

    # print(plot_data[0])
    # print(type(plot_data[0]), len(plot_data[0]))
    # print(plot_data[1])
    # print(type(plot_data[1]), len(plot_data[1]))
    # print(plot_data[2])
    # print(type(plot_data[2]))
    # print(plot_data[3])
    # print(type(plot_data[3]))
    # print(plot_data[4])
    # print(type(plot_data[4]))

    plot_vitals(plot_data[0], plot_data[1], plot_data[2], plot_data[3], plot_data[4])

    with open(os.path.join(client_root, "whole_files", pid + ".txt"), "w") as write_file:
        write_file.writelines(response_data)
        write_file.close()

    client_socket.close()


request("hl7", send_whole_file, plot_bool, patient, vital_p, t_from, t_to)
