import os
import matplotlib.pyplot as plot
import scouting
import datetime
import socket

t_from = "20110622092400"
t_to = "20110622095000"
patient = "2011024"
vital_p = "001000^VITAL HR"
parameter_list = scouting.unique_vitals_in_msgs


def datetime_from_msg(msg_time):
    d = datetime.datetime(int(msg_time[0:4]), int(msg_time[5:6]), int(msg_time[6:8]))
    t = datetime.time(int(msg_time[8:10]), int(msg_time[10:12]), int(msg_time[12:14]))
    combined = d.combine(d, t)
    return combined


def plot_vitals(pid, vital_parameter, time_from, time_to):
    vital_values = []
    time_at_observation = []
    units_measure = ""

    if not int(time_from) < int(time_to):
        return print("can't plot vital graph, incorrect time input")

    with open(os.path.join("_data_by_pid", pid), "r") as read_file:

        for line in read_file:
            segment = line.split("|")

            if segment[0] == "OBR" and int(time_from) <= int(segment[7]) <= int(time_to):
                one_block_check = True

            if segment[0] == "OBX" and segment[3] == vital_parameter and one_block_check:
                vital_values.append(int(segment[5]))
                time_at_observation.append(datetime_from_msg(segment[14]))
                units_measure = segment[6]
                one_block_check = False

    read_file.close()
    print("last times are: ", time_at_observation[-5:])
    print("last vitals are: " + str(vital_values[-5:]))
    plot.plot(time_at_observation, vital_values)
    plot.xlabel("time")
    plot.ylabel(units_measure)
    plot.title("patient " + pid + " " + vital_parameter)
    plot.show()


plot_vitals(patient, vital_p, t_from, t_to)
print(datetime_from_msg(t_from))
print(datetime.datetime(2011, 6, 22, 9, 45, 34))
