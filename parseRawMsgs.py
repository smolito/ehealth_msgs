import os
import scouting

data_root = "_raw_files"
segments_in_msgs = scouting.unique_segments_in_msgs


def parse_raw_msgs(file):
    with open(os.path.join(data_root, file), "r") as file_read:
        msg_block_buffer = []

        if not os.path.exists("_msgs_clean"):
            os.makedirs("_msgs_clean", exist_ok=True)

        if not os.path.exists("_data_by_pid"):
            os.makedirs("_data_by_pid", exist_ok=True)

        for fileline in file_read:
            prev_pid = ""
            segment = fileline.split("|")

            if segment[0] == "MSH":
                msg_block_start_id = segment[9].strip()

            if segment[0] == "PID":
                curr_pid = segment[3]
                if curr_pid == prev_pid or prev_pid == "":  # patient verification
                    prev_pid = curr_pid

            if segment[0] == "OBR":
                observation_end_datetime = segment[7].strip()

            if segment[0] == "OBX":

                if not segment[14].strip() == observation_end_datetime:  # observation verification
                    print("different observation times with patient:", curr_pid, "at", observation_end_datetime,
                          "in observation parameter", segment[3])

            if segments_in_msgs.__contains__(segment[0]):

                with open(os.path.join("_msgs_clean", file), "a") as clean_file_write:

                    clean_file_write.write(fileline)
                    msg_block_buffer.append(fileline)

                    if segment[0] == "MSA":
                        msg_block_end_id = segment[2].strip()

                        clean_file_write.write("\n")
                        clean_file_write.close()

                        # print(msg_block_end_id, msg_block_start_id)
                        if msg_block_start_id == msg_block_end_id:  # message end verification

                            with open(os.path.join("_data_by_pid", curr_pid), "a") as byPIDfile_write:
                                msg_block_buffer.append("\n")
                                byPIDfile_write.writelines(msg_block_buffer)
                                byPIDfile_write.close()
                                msg_block_buffer = []
                        else:
                            print("different ids at", msg_block_start_id, ", patient", curr_pid)

    file_read.close()


for single_file in os.listdir(os.path.join(data_root)):
    print("parsing raw", single_file, "right now")
    parse_raw_msgs(single_file)
