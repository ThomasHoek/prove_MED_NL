import re
from pathlib import Path

# get unparsed
# TODO: replace with parse data for produce
broken = open("MED_NL/broken_num.txt", "r").readlines()
broken = [int(x.rstrip()) for x in broken]
print(broken)

# get data
# TODO: replace with parse data for produce
split = "crowd"
result_path = f"Results/{split}"
analysis_path = f"{result_path}/analysis"

# TODO: replace with parse data for produce
file_info = open(f"{result_path}/alpino_aethel.alpino.log").readlines()
all_info = "".join([x.replace("\n", "|") for x in file_info])


def to_print(x: str) -> str:
    return x.replace("|", "\n")


# regex match and remove empty whitespace lines
# FIXME: ADD PARSING FOR ERROR
regex_match = r"(Inconsistency in node types \(entail\/8\)\||\d+:)"
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
y_u = open(f"{analysis_path}/yes_unknown.txt", "w+")
y_y = open(f"{analysis_path}/yes_yes.txt", "w+")
d_a = open(f"{analysis_path}/defected_aethel.txt", "w+")
d_o = open(f"{analysis_path}/defected_other.txt", "w+")


# extract data
def get_data_from_log(sent: str) -> tuple[str, str, str]:
    # sent = re.sub("[^a-zA-Z0-9_ ]", '', sent)
    sent = re.sub(" +", " ", sent)
    sent = sent.strip()
    split_sent: list[str] = sent.split(" ")

    # remove comma for target, predict and solve
    split_sent[0:2] = [x.replace(",", "").strip() for x in split_sent[0:2]]

    target = split_sent[0][1:-1]
    predict = split_sent[1]
    other = " ".join(split_sent[2:])

    return target, predict, other


# for i in re_split[:10]:
#     print(i)

re_split_length = len(re_split)
index_pointer = 0
defected_flag = False
aethel_flag = False

while index_pointer != re_split_length:
    defected_flag = False
    aethel_flag = False
    prior_text = ""

    cur_line = re_split[index_pointer]
    while not cur_line[:-1].isdigit():
        if "Inconsistency" in cur_line:
            defected_flag = True

        # keep error data
        prior_text += cur_line

        # goto number
        index_pointer += 1
        cur_line = re_split[index_pointer]

    # check if number in aethel
    number_info = cur_line
    if int(cur_line[:-1]) in broken:
        aethel_flag = True

    # get info and paste info file
    index_pointer += 1
    cur_line = re_split[index_pointer]
    target, predict, other = get_data_from_log(cur_line)

    match (defected_flag, target, predict):
        case (True, _, _):
            if aethel_flag:
                file = d_a
            else:
                file = d_o
        case (False, "unknown", "unknown"):
            file = u_u

        case (False, "unknown", "yes"):
            file = u_y

        case (False, "yes", "unknown"):
            file = y_u

        case (False, "yes", "yes"):
            file = y_y

        case _:
            raise NotImplementedError("Should not reachthis")

    file.write(to_print(prior_text))
    file.write(to_print(number_info))
    file.write(to_print(cur_line))
    file.write("\n")

    index_pointer += 1
    print(index_pointer, re_split_length)
