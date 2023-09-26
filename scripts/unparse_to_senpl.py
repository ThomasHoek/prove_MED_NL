import re
from collections import Counter

sen_pl = open("MED_NL/sen.pl", "r").readlines()
# sen_pl = [x.rstrip() for x in sen_pl]


unparsed = open("MED_NL/unparse.txt", "r")
unparsed = [int(re.findall("[0-9]+", x)[0]) for x in unparsed]


def grep(inp_lst: list[str], inp_str: str) -> int:
    # https://stackoverflow.com/a/53537365
    ide = [i for i, item in enumerate(inp_lst) if re.search(inp_str, item)]
    return ide[0]


num_lst: list[int] = []
for i in unparsed:
    sen_index = grep(sen_pl, f"%problem id = {i}\n")
    for plus in [1, 2]:
        num_lst.append(
            int(sen_pl[sen_index + plus].split(",")[0].replace("sen_id(", ""))
        )


with open("MED_NL/broken.txt", "w+") as broken:
    for k, v in Counter(num_lst).most_common():
        broken.write("{} - {}\n".format(k, v))

with open("MED_NL/broken_num.txt", "w+") as broken_num:
    for line in Counter(num_lst):
        broken_num.write(f"{line}\n")
