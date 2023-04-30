import os
import matplotlib.pyplot as plot
import scouting
from datetime import datetime, date, time, timezone

t_from = "20110803092503"
t_to = "20110803092803"
patient = "2011033"
vital_p = "001000^VITAL HR"
parameter_list = scouting.unique_vitals_in_msgs


def datetime_from_msg(msg_time):
    d = date(int(msg_time[0:4]), int(msg_time[4:6]), int(msg_time[6:8]))
    t = time(int(msg_time[8:10]), int(msg_time[10:12]), int(msg_time[12:14]))
    return datetime.combine(d, t)


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

    plot.plot(time_at_observation, vital_values)
    plot.xlabel("time")
    plot.ylabel(units_measure)
    plot.title("patient " + pid + " " + vital_parameter)
    plot.show()


plot_vitals(patient, vital_p, t_from, t_to)
print(datetime_from_msg(t_from))
