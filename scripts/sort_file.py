from itertools import groupby
import re


all_file_paths: list[str] = [
    "Results/crowd/analysis/defected_aethel.txt",
    "Results/crowd/analysis/defected_cp.txt",
    "Results/crowd/analysis/defected_other.txt",
    "Results/crowd/analysis/defected_sv1.txt",
    "Results/crowd/analysis/error.txt",
    "Results/crowd/analysis/incorrect_str.txt",
    "Results/crowd/analysis/unknown_no.txt",
    "Results/crowd/analysis/unknown_unknown.txt",
    "Results/crowd/analysis/unknown_yes.txt",
    "Results/crowd/analysis/yes_no.txt",
    "Results/crowd/analysis/yes_unknown.txt",
    "Results/crowd/analysis/yes_yes.txt",
]


def sort_file(path: str):
    def find_id(inp_raw: list[str]) -> int:
        return int(re.search("\d+:", "".join(inp_raw)).group()[:-1])

    file_read = open(path)
    file_info = file_read.readlines()
    file_read.close()

    file_group = [
        list(group)
        for key, group in groupby(file_info, lambda x: x == " \n" or x == "\n")
        if not key
    ]

    dict_problem = {}
    for i in file_group:
        dict_problem[find_id(i)] = i

    write_file = open(path, "w+")
    for key in sorted(dict_problem):
        write_file.write(f"{''.join(dict_problem[key])}\n")


if __name__ == "__main__":
    all_file_paths: list[str] = [
        "Results/crowd/analysis/defected_aethel.txt",
        "Results/crowd/analysis/defected_cp.txt",
        "Results/crowd/analysis/defected_other.txt",
        "Results/crowd/analysis/defected_sv1.txt",
        "Results/crowd/analysis/error.txt",
        "Results/crowd/analysis/incorrect_str.txt",
        "Results/crowd/analysis/unknown_no.txt",
        "Results/crowd/analysis/unknown_unknown.txt",
        "Results/crowd/analysis/unknown_yes.txt",
        "Results/crowd/analysis/yes_no.txt",
        "Results/crowd/analysis/yes_unknown.txt",
        "Results/crowd/analysis/yes_yes.txt",
    ]

    for x in all_file_paths:
        sort_file(x)
