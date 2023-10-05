import os
import ast
from collections import Counter


def find_broken_phrase(phrase: str) -> list[int]:
    """To be fixed so no need for modular"""

    def to_int(pl_str: str) -> int:
        return int(pl_str.split(",")[0][1:])

    alpino_pl = open("MED_NL/parses/alpino_aethel.pl", "r").readlines()
    alpino_pl = "".join(alpino_pl).split("sen_id_tlg_tok")[1:]

    # number path_name -> split on space and first bit to int
    max_problems = int(os.popen("wc -l MED_NL/raw.spl").read().split(" ")[0])

    # set range to max_problems as False -> False; not encountered
    truth_table = dict(zip(range(1, max_problems), [False] * max_problems))

    # set all found numbers to true
    for line in alpino_pl:
        truth_table[to_int(line)] = phrase in line

    # remove True values, keep keys
    broken_sent = sorted(list({int(k) for k, v in truth_table.items() if v is True}))

    # write all
    broken_phrase = open(f"MED_NL/problems/broken_{phrase}.txt", "w+")
    broken_phrase.writelines(str(line) + "\n" for line in broken_sent)
    return broken_sent


def get_missing_numbers(
    alpino_path: str, raw_path: str, broken_sent_path: str
) -> list[int]:
    def to_int(pl_str: str) -> int:
        return int(pl_str.split(",")[0][1:])

    alpino_pl = open(alpino_path, "r").readlines()
    alpino_pl = "".join(alpino_pl).split("sen_id_tlg_tok")[1:]

    # number path_name -> split on space and first bit to int
    max_problems = int(os.popen(f"wc -l {raw_path}").read().split(" ")[0])
    print(max_problems)

    # set range to max_problems as False -> False; not encountered
    truth_table = dict(zip(range(1, max_problems), [False] * max_problems))

    # set all found numbers to true
    for line in alpino_pl:
        truth_table[to_int(line)] = True

    # remove True values, keep keys
    broken_sent = sorted(
        list({int(k) for k, v in truth_table.items() if v is not True})
    )

    # write all
    broken_sen_pl = open(broken_sent_path, "w+")
    broken_sen_pl.writelines(str(line) + "\n" for line in broken_sent)

    return broken_sent


def get_missing_text(
    alpino_path: str, raw_path: str, broken_sent_path: str
) -> list[int]:
    def to_int(pl_str: str) -> int:
        return int(pl_str.split(",")[0][1:])

    def to_str(pl_str: str) -> str:
        list_in_list_str = pl_str.split(r"),")[-1].split("\n")[1]
        list_in_list = ast.literal_eval(list_in_list_str)
        list_single = list(map("".join, list_in_list))
        single_str = "".join(list_single)
        return single_str

    alpino_pl = open(alpino_path, "r").readlines()
    alpino_pl = "".join(alpino_pl).split("sen_id_tlg_tok")[1:]

    # number path_name -> split on space and first bit to int
    raw_sp_read = open(raw_path, "r").readlines()
    raw_sp_read = [x.rstrip().replace(" ", "") for x in raw_sp_read]

    # set range to max_problems as False -> False; not encountered
    truth_table = dict(zip(range(1, len(raw_sp_read)), [False] * len(raw_sp_read)))

    # set all found numbers to true
    debug_file = open(broken_sent_path.replace(".txt", "_debug.txt"), "w+")
    for line in alpino_pl:
        cur_index = to_int(line)
        if not to_str(line) == raw_sp_read[cur_index - 1]:
            debug_file.writelines(f"------------{cur_index}------------\n")
            debug_file.writelines(to_str(line))
            debug_file.writelines("\n")
            debug_file.writelines(raw_sp_read[cur_index - 1])
            debug_file.writelines("\n")

            truth_table[cur_index] = True

    # remove True values, keep keys
    broken_sent = sorted(list({int(k) for k, v in truth_table.items() if v is True}))

    # write all
    broken_sen_pl = open(broken_sent_path, "w+")
    broken_sen_pl.writelines(str(line) + "\n" for line in broken_sent)

    return broken_sent


def sen_pl_comments(sen_pl_path: str, broken_sen_pl_path: str) -> list[int]:
    num_set: set[int] = set()
    for prob_line in open(sen_pl_path, "r").readlines():
        if prob_line[0] == "%":
            # check if number:
            if "%problem" in prob_line:
                continue

            prob_line = prob_line[1:]

            sent_id, problem_id = prob_line.split(",")[0:2]
            problem_id = int(problem_id)
            sent_id = int(sent_id.replace("sen_id(", ""))

            num_set.add(problem_id)

    num_lst: list[int] = sorted(list(num_set))

    with open(broken_sen_pl_path, "w+") as broken:
        for line in Counter(num_lst):
            broken.write(f"{line}\n")

    return num_lst


def problem_to_sent(problem_lst: list[int], sen_pl_path: str, broken_path: str) -> None:
    num_lst: list[int] = []
    for prob_line in open(sen_pl_path, "r").readlines():
        if prob_line[0] == "%":
            # check if number:
            if "%problem" in prob_line:
                continue

            prob_line = prob_line[1:]

        sent_id, problem_id = prob_line.split(",")[0:2]
        problem_id = int(problem_id)
        sent_id = int(sent_id.replace("sen_id(", ""))

        if sent_id in problem_lst:
            num_lst.append(problem_id)

    with open(broken_path, "w+") as broken:
        for line in Counter(num_lst):
            broken.write(f"{line}\n")

    broken_path = broken_path.replace(".txt", "_count.txt")
    with open(broken_path, "w+") as broken:
        for k, v in Counter(num_lst).most_common():
            broken.write("{} - {}\n".format(k, v))


def sent_to_problem(sent_lst: list[int], sen_pl_path: str, broken_path: str) -> None:
    num_lst: list[int] = []
    for prob_line in open(sen_pl_path, "r").readlines():
        if prob_line[0] == "%":
            # check if number:
            if "%problem" in prob_line:
                continue

            prob_line = prob_line[1:]

        sent_id, problem_id = prob_line.split(",")[0:2]
        problem_id = int(problem_id)
        sent_id = int(sent_id.replace("sen_id(", ""))

        if sent_id in sent_lst:
            num_lst.append(problem_id)

    num_lst.sort()
    with open(broken_path, "w+") as broken:
        for line in Counter(num_lst):
            broken.write(f"{line}\n")

    broken_path = broken_path.replace(".txt", "_count.txt")
    with open(broken_path, "w+") as broken:
        for k, v in Counter(num_lst).most_common():
            broken.write("{} - {}\n".format(k, v))


# general
sen_pl = "MED_NL/sen.pl"
raw_sp = "MED_NL/raw.spl"

# alpino
alpino_path = "MED_NL/parses/alpino_aethel.pl"
broken_alpino = "MED_NL/problems/broken_alpino_aethel.txt"
broken_alpino_sent = "MED_NL/problems/broken_alpino_aethel_sentences.txt"
missing_num: list[int] = get_missing_numbers(alpino_path, raw_sp, broken_alpino)
problem_to_sent(missing_num, sen_pl, broken_alpino_sent)

# alpino2
alpino_path = "MED_NL/parses/alpino_aethel.pl"
broken_alpino = "MED_NL/problems/broken_alpino_aethel_sent.txt"
broken_alpino_sent = "MED_NL/problems/broken_alpino_aethel_sent_sentences.txt"
missing_num: list[int] = get_missing_text(alpino_path, raw_sp, broken_alpino)
sent_to_problem(missing_num, sen_pl, broken_alpino_sent)


# sen_pl
broken_sent = "MED_NL/problems/broken_sen_pl.txt"
broken_alpino_sent = "MED_NL/problems/broken_sen_pl_sentences.txt"
missing_num = sen_pl_comments(sen_pl, broken_sent)
problem_to_sent(missing_num, sen_pl, broken_alpino_sent)


# remove when done
broken_conj = "MED_NL/problems/broken_cp_problems.txt"
missing_num = find_broken_phrase("cp")
sent_to_problem(missing_num, sen_pl, broken_conj)

# remove when done
broken_sv = "MED_NL/problems/broken_sv1_problems.txt"
missing_num = find_broken_phrase("sv1")
sent_to_problem(missing_num, sen_pl, broken_sv)
