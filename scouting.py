# script written to explore data in messages

import os

data_root = "_raw_files"


def get_unique_segment_names(file):
    with open(os.path.join(data_root, file), "r") as file_read:
        segments = []

        for line in file_read:
            parts = line.split("|")
            segments.append(parts[0])

        unique_segments = [
            item for item in segments
            if len(item) == 3
        ]
        unique_segments = set(unique_segments)

        return unique_segments


unique_segments_in_msgs = []

for single_file in os.listdir(os.path.join(data_root)):
    single_set = get_unique_segment_names(single_file)
    set2list = list(single_set)
    unique_segments_in_msgs = unique_segments_in_msgs + set2list
    print(set(unique_segments_in_msgs))

unique_segments_in_msgs = set(unique_segments_in_msgs)
unique_segments_in_msgs = list(unique_segments_in_msgs)
print("whole ", unique_segments_in_msgs)

# set(unique_segments_in_msgs)
#
# if unique_segments_in_msgs.__contains__("MSA"):
#     print("msa included")
# else:
#     print("nah")
