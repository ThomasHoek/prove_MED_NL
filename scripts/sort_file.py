from itertools import groupby
import re


def sort_file(path: str) -> None:
    def find_id(inp_raw: list[str]) -> int:
        return int(re.search(r"\d+:", "".join(inp_raw)).group()[:-1])

    file_read = open(path)
    file_info = file_read.readlines()
    file_read.close()

    file_group: list[list[str]] = [
        list(group)
        for key, group in groupby(file_info, lambda x: x == " \n" or x == "\n")
        if not key
    ]

    dict_problem: dict[int, list[str]] = {}
    for i in file_group:
        dict_problem[find_id(i)] = i

    write_file = open(path, "w+")
    for key in sorted(dict_problem):
        write_file.write(f"{''.join(dict_problem[key])}\n")


if __name__ == "__main__":
    import glob
    all_file_paths: list[str] = glob.glob('Results/crowd/analysis/*.txt')

    for x in all_file_paths:
        sort_file(x)
