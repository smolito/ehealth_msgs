import os
import scouting

data_root = "_raw_files"
segments_in_msgs = scouting.unique_segments_in_msgs

def parse_raw_msgs(file):
    with open(os.path.join(data_root, file), "r") as file_read:
        line = []

        if not os.path.exists("_msgs"):
            os.makedirs("_msgs", exist_ok=True)

        for fileline in file_read:
            segment = fileline.split("|")


# for single_file in os.listdir(os.path.join(data_root)):
