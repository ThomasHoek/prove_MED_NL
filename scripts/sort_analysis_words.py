from itertools import groupby
from collections import Counter
import re


def sort_file_words(path: str) -> None:
    file_read = open(path)
    file_info = file_read.readlines()
    file_read.close()

    file_group = [
        list(group)
        for key, group in groupby(file_info, lambda x: x == " \n" or x == "\n")
        if not key
    ]

    word_counter: Counter[str] = Counter()
    for i in file_group:
        sents = i[-2:]
        for sent in sents:
            split_sent = re.sub(r"[^\w]", " ", sent).split()
            word_counter.update([x.lower() for x in split_sent])

    new_path = path.replace("analysis", "detailed")
    with open(new_path, "w+") as write_file:
        for k, v in word_counter.most_common():
            write_file.write("{} {}\n".format(k, v))


if __name__ == "__main__":
    import glob
    import os

    all_file_paths: list[str] = glob.glob("Results/crowd/analysis/*.txt")

    if not os.path.exists("Results/crowd/detailed"):
        os.makedirs("Results/crowd/detailed")

    for x in all_file_paths:
        sort_file_words(x)
