import argparse
import os
import ast
from utils import generator_sen_problem_ID, write_to_file


def find_broken_phrase(
    alpino_path: str, raw_path: str, phrase: str, output_path: str
) -> list[int]:

    def to_int(pl_str: str) -> int:
        # splits alpino problem on , and removes the bracket infront of the number.
        return int(pl_str.split(",")[0][1:])

    alpino_pl = open(alpino_path, "r").readlines()
    alpino_pl = "".join(alpino_pl).split("sen_id_tlg_tok")[1:]

    # wc -l -> outputs "length of file | path_name"
    # split on space ("|") in comment and first bit to int
    max_problems = int(os.popen(f"wc -l {raw_path}").read().split(" ")[0])

    # set range to max_problems as False -> False; not encountered
    truth_table = dict(zip(range(1, max_problems), [False] * max_problems))

    # set all found numbers to true
    for line in alpino_pl:
        truth_table[to_int(line)] = phrase in line

    # remove False values, keep keys
    broken_sent = sorted(list({int(k) for k, v in truth_table.items() if v is True}))

    # write all
    broken_sen_pl = open(output_path, "w+")
    broken_sen_pl.writelines(str(line) + "\n" for line in broken_sent)

    return broken_sent


def get_missing_numbers(alpino_path: str, raw_path: str, output_path: str) -> list[int]:
    """
    get_missing_numbers Finds numbers that appears in alpino, writes missing to file

    Args:
        alpino_path (str): alpino path
        raw_path (str): raw.spl path
        output_path (str): output path

    Returns:
        list[int]: list of missing sentence numbers
    """

    def to_int(pl_str: str) -> int:
        return int(pl_str.split(",")[0][1:])

    alpino_pl = open(alpino_path, "r").readlines()
    alpino_pl = "".join(alpino_pl).split("sen_id_tlg_tok")[1:]

    # wc -l -> outputs "length of file | path_name"
    # split on space ("|") in comment and first bit to int
    max_problems = int(os.popen(f"wc -l {raw_path}").read().split(" ")[0])

    # set range to max_problems as False -> False; not encountered
    truth_table = dict(zip(range(1, max_problems), [False] * max_problems))

    # set all found numbers to true
    for line in alpino_pl:
        truth_table[to_int(line)] = True

    # remove True values, keep keys
    broken_sent = sorted(list({int(k) for k, v in truth_table.items() if v is False}))

    # write all
    broken_sen_pl = open(output_path, "w+")
    broken_sen_pl.writelines(str(line) + "\n" for line in broken_sent)

    return broken_sent


def get_missing_text(
    alpino_path: str, raw_path: str, output_path: str, verbose: bool = False
) -> list[int]:
    """
    get_missing_text finds problem numbers where the Alpino_aether parser messed up

    In some problems alpino_aether eats away the start or the end of sentences.
    This function finds the raw sentence and checks it with alpino.
    This is done without spaces due to alpino merging words.

    Args:
        alpino_path (str): Path to alpino file
        raw_path (str): Path to raw.spl
        output_path (str): path to write output to

    Returns:
        list[int]: list of sentence Id's that have problems
    """

    def to_int(pl_str: str) -> int:
        # splits alpino into a int
        return int(pl_str.split(",")[0][1:])

    def to_str(pl_str: str) -> str:
        # clean PL string to only string list of words
        list_in_list_str = pl_str.split(r"),")[-1].split("\n")[1]
        # convert string list to actual list
        list_in_list = ast.literal_eval(list_in_list_str)
        # list in lists to single list
        list_single = list(map("".join, list_in_list))
        # single list to string
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
    debug_file = open(output_path.replace(".txt", "_debug.txt"), "w+")
    for line in alpino_pl:
        cur_index = to_int(line)
        # -1 because alpino & sen.pl start at 1
        if not to_str(line) == raw_sp_read[cur_index - 1]:
            if verbose:
                debug_file.writelines(f"------------{cur_index}------------\n")
                debug_file.writelines(to_str(line))
                debug_file.writelines("\n")
                debug_file.writelines(raw_sp_read[cur_index - 1])
                debug_file.writelines("\n")

            truth_table[cur_index] = True

    # remove True values, keep keys
    broken_sent = sorted(list({int(k) for k, v in truth_table.items() if v is True}))

    # write all
    broken_sen_pl = open(output_path, "w+")
    broken_sen_pl.writelines(str(line) + "\n" for line in broken_sent)

    return broken_sent


def sen_pl_comments(sen_pl_path: str, output_path: str) -> list[int]:
    """
    sen_pl_comments find commented lines in sen_pl

    Args:
        sen_pl_path (str): path to sen_pl
        output_path (str): path to write output

    Returns:
        list[int]: list of missing problems
    """
    num_set: set[int] = set()
    for prob_line in open(sen_pl_path, "r").readlines():
        if prob_line[0] == "%":
            # check if number:
            if "%problem" in prob_line:
                continue

            _, problem_id = prob_line[1:].split(",")[0:2]
            problem_id = int(problem_id)
            num_set.add(problem_id)

    num_lst: list[int] = sorted(list(num_set))

    write_to_file(num_lst, output_path)

    return num_lst


def problem_to_sent(
    problem_lst: list[int], sen_pl_path: str, output_path: str, verbose: bool = False
) -> None:
    """
    problem_to_sent List of problem id's to sentences in file

    Args:
        problem_lst (list[int]):list of problem IDs
        sen_pl_path (str): sen_pl path
        broken_path (str): output path
    """
    num_lst: list[int] = []

    # generator for sent and problem ID
    for sent_id, problem_id in generator_sen_problem_ID(sen_pl_path):
        if problem_id in problem_lst:
            num_lst.append(sent_id)

    write_to_file(num_lst, output_path, verbose)


def sent_to_problem(
    sent_lst: list[int], sen_pl_path: str, output_path: str, verbose: bool = False
) -> None:
    """
    sent_to_problem Translates a list of sentences to problem numbers in file

    Args:
        sent_lst (list[int]): list with sentence integers
        sen_pl_path (str): path to sen_pl
        broken_path (str): path to write output
    """

    num_lst: list[int] = []
    # generator for sent and problem ID
    for sent_id, problem_id in generator_sen_problem_ID(sen_pl_path):
        # if sentence ID found in sentence list
        if sent_id in sent_lst:
            num_lst.append(problem_id)

    write_to_file(num_lst, output_path, verbose)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Finds problems in dataset"
    )

    # Arguments covering directories and files
    parser.add_argument("sen_pl", metavar="SEN_PL", help="The path to sen_pl")
    parser.add_argument("raw_sp", metavar="RAW_PATH", help="The path to raw.spl")
    parser.add_argument("alpino_path", metavar="ALPINO_PATH", help="The path to alpino_aethel.pl")
    parser.add_argument("output_path", metavar="OUTPUT_PATH", help="A directory to write the outputs to")
    parser.add_argument("verbose", metavar="VERBOSE", help="print extra files")

    # pre-processing arguments
    args = parser.parse_args()
    return args


##############################################################################
################################ Main function ################################
if __name__ == "__main__":
    args = parse_arguments()

    # args.output_path = args.output_path[:-1]
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    # alpino
    broken_alpino_s = f"{args.output_path}/alpino_number_missing_sen.txt"
    broken_alpino_p = f"{args.output_path}/alpino_number_missing_prob.txt"
    missing_num: list[int] = get_missing_numbers(args.alpino_path, args.raw_sp, broken_alpino_s)
    sent_to_problem(missing_num, args.sen_pl, broken_alpino_p, args.verbose)

    # # alpino2
    broken_alpino_p = f"{args.output_path}/alpino_text_missing_prob.txt"
    broken_alpino_s = f"{args.output_path}/alpino_text_missing_sen.txt"
    missing_num: list[int] = get_missing_text(args.alpino_path, args.raw_sp, broken_alpino_p, args.verbose)
    problem_to_sent(missing_num, args.sen_pl, broken_alpino_s, args.verbose)

    # sen_pl
    broken_sent_p = f"{args.output_path}/sen_pl_prob.txt"
    broken_sent_s = f"{args.output_path}/sen_pl_sen.txt"
    missing_num = sen_pl_comments(args.sen_pl, broken_sent_p)
    problem_to_sent(missing_num, args.sen_pl, broken_sent_s, args.verbose)

    # broken phrases
    phrases = ["cp", "sv1"]
    for phrase in phrases:
        phrase_output_s = f"{args.output_path}/phrase_{phrase}_sent.txt"
        phrase_output_p = f"{args.output_path}/phrase_{phrase}_prob.txt"
        missing_num = find_broken_phrase(args.alpino_path, args.raw_sp, phrase, phrase_output_s)
        sent_to_problem(missing_num, args.sen_pl, phrase_output_p, args.verbose)
