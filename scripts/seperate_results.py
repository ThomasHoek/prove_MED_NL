import re
from pathlib import Path
import argparse
import os


def to_print(x: str) -> str:
    """to_print removes regex preprocessing"""
    return x.replace("|", "\n")


# extract data
def get_data_from_log(sent: str) -> tuple[str, str, str]:
    """
    get_data_from_log parses the data from log files to labels

    Args:
        sent (str): sentence with label info

    Returns:
        tuple[str, str, str]: two labels and the rest of the information
    """
    # remove whitespace
    sent = re.sub(" +", " ", sent)
    sent = sent.strip()

    # split based on space
    split_sent: list[str] = sent.split(" ")

    # remove comma for target, predict and solve
    split_sent[0:2] = [x.replace(",", "").strip() for x in split_sent[0:2]]

    # get info and merge rest back together
    target = split_sent[0][1:-1]
    predict = split_sent[1]
    other = " ".join(split_sent[2:])

    return target, predict, other


# MAIN Function
# TODO: replace with parse data for produce
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-k", "--kind", default="crowd", help="select result kind")

# Read arguments from command line
args = parser.parse_args()
split = args.kind


# get data
def file_to_int_lst(path_str: str) -> list[int]:
    return [int(x.rstrip()) for x in open(path_str, "r").readlines()]


result_path = f"Results/{split}"
analysis_path = f"{result_path}/analysis"

broken_conj = file_to_int_lst("MED_NL/problems/broken_cp_problems.txt")
broken_sv = file_to_int_lst("MED_NL/problems/broken_sv1_problems.txt")
broken_unparse = file_to_int_lst("MED_NL/problems/broken_alpino_aethel_sentences.txt")
broken_string = file_to_int_lst("MED_NL/problems/broken_alpino_aethel_sent_sentences.txt")


# open files from input
file_info = open(f"{result_path}/alpino_aethel.alpino.log").readlines()
all_info = "".join([x.replace("\n", "|") for x in file_info])

# regex match and remove empty whitespace lines
regex_match = r"(ERROR|Error|Inconsistency in node types \(entail\/8\)\||\d+:)"
re_split = re.split(regex_match, all_info)
re_split = [x for x in re_split if x.rstrip()]
meta_data = to_print(re_split.pop(0))

# seperate results from line
re_split[-1] = re_split[-1].split(
    "------------------------------------------------------"
)[0]

# make folders and data
Path(f"{analysis_path}").mkdir(parents=True, exist_ok=True)
u_u = open(f"{analysis_path}/unknown_unknown.txt", "w+")
u_y = open(f"{analysis_path}/unknown_yes.txt", "w+")
u_n = open(f"{analysis_path}/unknown_no.txt", "w+")

y_u = open(f"{analysis_path}/yes_unknown.txt", "w+")
y_y = open(f"{analysis_path}/yes_yes.txt", "w+")
y_n = open(f"{analysis_path}/yes_no.txt", "w+")

# defected files
d_a = open(f"{analysis_path}/defected_aethel.txt", "w+")
d_cp = open(f"{analysis_path}/defected_cp.txt", "w+")
d_sv = open(f"{analysis_path}/defected_sv1.txt", "w+")
d_o = open(f"{analysis_path}/defected_other.txt", "w+")

# all errrors
error_file = open(f"{analysis_path}/error.txt", "w+")
incorrect_str = open(f"{analysis_path}/incorrect_str.txt", "w+")

# set flags and size
re_split_length = len(re_split)
index_pointer = 0
while index_pointer != re_split_length:
    defected_flag = False
    aethel_flag = False
    error_flag = False
    conj_flag = False
    sv1_flag = False
    string_flag = False
    prior_text = ""

    # get first / next line
    cur_line = re_split[index_pointer]

    # error, inconsistant etc messages
    while not cur_line[:-1].isdigit():
        if "error" in cur_line.lower():
            error_flag = True

        if "Inconsistency" in cur_line:
            defected_flag = True

        # keep error data
        prior_text += cur_line

        # stay in loop until number is found
        index_pointer += 1
        cur_line = re_split[index_pointer]

    # check if number in aethel
    number_info = cur_line
    num = int(cur_line[:-1])
    if num in broken_unparse:
        aethel_flag = True
    elif num in broken_conj:
        conj_flag = True
    elif num in broken_sv:
        sv1_flag = True

    if num in broken_string:
        string_flag = True

    # get info and paste info file
    index_pointer += 1
    cur_line = re_split[index_pointer]
    target, predict, other = get_data_from_log(cur_line)

    # match to find correct file to write to
    match (defected_flag, target, predict):
        case (True, _, _):
            if aethel_flag:
                file = d_a
            elif conj_flag:
                file = d_cp
            elif sv1_flag:
                file = d_sv
            else:
                file = d_o
        case (False, "unknown", "unknown"):
            file = u_u

        case (False, "unknown", "yes"):
            file = u_y

        case (False, "unknown", "no"):
            file = u_n

        case (False, "yes", "unknown"):
            file = y_u

        case (False, "yes", "yes"):
            file = y_y

        case (False, "yes", "no"):
            file = y_n

        case _:
            print(defected_flag, target, predict)
            raise NotImplementedError("Should not reach this")

    # write all info to file
    file.write(to_print(prior_text))
    file.write(to_print(number_info))
    file.write(to_print(cur_line))
    file.write("\n")

    # error tracking
    if error_flag:
        error_file.write(to_print(prior_text))
        error_file.write(to_print(number_info))
        error_file.write(to_print(cur_line))
        error_file.write("\n")

    if string_flag:
        incorrect_str.write(to_print(prior_text))
        incorrect_str.write(to_print(number_info))
        incorrect_str.write(to_print(cur_line))
        incorrect_str.write("\n")

    index_pointer += 1

for i in [u_u, u_y, u_n,  y_u, y_y, y_n, d_a, d_cp, d_sv, d_o, error_file, incorrect_str]:
    i.close()

os.system(f"/bin/python {os.getcwd()}/scripts/sort_file.py")
