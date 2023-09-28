import re
from collections import Counter

sen_pl = open("MED_NL/sen.pl", "r").readlines()
# sen_pl = [x.rstrip() for x in sen_pl]


unparsed = open("MED_NL/unparse.txt", "r")
unparsed = [int(re.findall("[0-9]+", x)[0]) for x in unparsed]


num_lst: list[int] = []
for prob_line in sen_pl:
    if prob_line[0] == "%":
        continue

    print(prob_line)
    sent_id, problem_id = prob_line.split(",")[0:2]
    problem_id = int(problem_id)
    sent_id = int(sent_id.replace("sen_id(", ""))

    if sent_id in unparsed:
        num_lst.append(problem_id)


with open("MED_NL/broken.txt", "w+") as broken:
    for k, v in Counter(num_lst).most_common():
        broken.write("{} - {}\n".format(k, v))

with open("MED_NL/broken_num.txt", "w+") as broken_num:
    for line in Counter(num_lst):
        broken_num.write(f"{line}\n")
