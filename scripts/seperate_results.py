import re

file_info = open("Results/HELP/alpino_aethel.alpino.log").readlines()
all_info = ''.join([x.replace("\n", "|") for x in file_info])
# all_info = ''.join(file_info)
# regex_match = r"(\d+:|Inconsistency in node types \(entail\/8\))"
# (\r\n|\n|\r)
regex_match = r"(Inconsistency in node types \(entail\/8\)\| *\d+:|\d+:)"
re_split = re.split(regex_match, all_info)


for i in range(15):
    print(rf"{i} || {re_split[i]}")