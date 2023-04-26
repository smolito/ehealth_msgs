import os

data_root = "_raw_files"


def parse_raw_msgs(file):
    with open(os.path.join(data_root, file), "r") as file_read:
        line = []

        for fileline in file_read:
            parts = line.split("|")
            line.append(parts[0])

        unique_segments = [
            item for item in segments
            if len(item) == 3
        ]
        unique_segments = set(unique_segments)

        return unique_segments

# for single_file in os.listdir(os.path.join(data_root)):
