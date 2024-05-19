import subprocess, os
import pandas as pd
from itertools import chain
import os
from glob import glob

BASH_CONVERT_COMMAND = "makemkvcon mkv --robot 'PATH_VIDEO_TS' all 'OUTPUT_FOLDER'"


def get_convert_command(file, output_path):
    command = BASH_CONVERT_COMMAND.replace("PATH_VIDEO_TS", file.replace("'", r"'\''"))
    command = command.replace("OUTPUT_FOLDER", output_path)
    return command


def get_video_list(paths: list, file_name="VIDEO_TS.IFO"):
    df = pd.DataFrame()
    for dirpath, dirnames, filenames in chain.from_iterable(
        os.walk(path) for path in paths
    ):
        filenames = list(filter(lambda x: x == file_name, filenames))
        if filenames:
            filenames.sort()
            tmp = pd.DataFrame(
                {"dirpath": dirpath, "filenames": [filenames], "converted": False}
            )
            df = pd.concat([df, tmp], ignore_index=True)
    return df


def convert_video(file, output_path):
    command = get_convert_command(file, output_path)
    subprocess.check_output(command, shell=True, executable="/bin/bash")


def main(args):
    video_paths = get_video_list(args.paths)
    for index, row in video_paths.iterrows():
        input_path = row["dirpath"] + "/" + row["filenames"][0]
        output_path = row["dirpath"] + "/"
        command = get_convert_command(input_path, output_path)
        print(command)
        try:
            convert_video(
                input_path, output_path
            )
            video_paths.loc[index, ("converted")] = True
        except Exception as e: print(e)
    video_paths.to_csv("stats.csv")


from collections import namedtuple

Args = namedtuple("arg", ["paths"])

arg_in = Args(["videos/"])
main(arg_in)
