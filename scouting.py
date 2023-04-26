# script written to analyze data in messages
# test

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


for single_file in os.listdir(os.path.join(data_root)):
    print(get_unique_segment_names(single_file))

