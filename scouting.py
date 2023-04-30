# script written to explore data in messages

import os

data_root = "_raw_files"


def get_unique_segment_names(file):
    with open(os.path.join(data_root, file), "r") as file_read:
        segments = []
        vital_parameters = []

        for line in file_read:
            parts = line.split("|")
            segments.append(parts[0])

            if parts[0] == "OBX":
                vital_parameters.append(parts[3].strip())

        unique_parameters = set(vital_parameters)

        unique_segments = [
            item for item in segments
            if len(item) == 3
        ]
        unique_segments = set(unique_segments)
        file_read.close()
        return unique_segments, unique_parameters


unique_segments_in_msgs = []
unique_vitals_in_msgs = []


for single_file in os.listdir(os.path.join(data_root)):
    names_single_set = get_unique_segment_names(single_file)[0]
    parameter_single_set = get_unique_segment_names(single_file)[1]
    names_set2list = list(names_single_set)
    parameters_set2list = list(parameter_single_set)
    unique_segments_in_msgs = unique_segments_in_msgs + names_set2list
    unique_vitals_in_msgs = unique_vitals_in_msgs + parameters_set2list

unique_segments_in_msgs = set(unique_segments_in_msgs)
unique_segments_in_msgs = list(unique_segments_in_msgs)
unique_vitals_in_msgs = set(unique_vitals_in_msgs)
unique_vitals_in_msgs = list(unique_vitals_in_msgs)
