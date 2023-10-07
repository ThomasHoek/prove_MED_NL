from collections import Counter


def generator_sen_problem_ID(sen_pl_path: str):
    for prob_line in open(sen_pl_path, "r").readlines():
        if prob_line[0] == "%":
            # check if number:
            if "%problem" in prob_line:
                continue

            prob_line = prob_line[1:]

        sent_id, problem_id = prob_line.split(",")[0:2]
        problem_id = int(problem_id)
        sent_id = int(sent_id.replace("sen_id(", ""))
        yield sent_id, problem_id


def write_to_file(num_lst: list[int], output_path: str, verbose: bool = False) -> None:
    # sentences to file
    num_lst.sort()
    with open(output_path, "w+") as broken:
        for line in Counter(num_lst):
            broken.write(f"{line}\n")

    # sentences_count to file
    if verbose:
        output_path = output_path.replace(".txt", "_count.txt")
        with open(output_path, "w+") as broken:
            for k, v in Counter(num_lst).most_common():
                broken.write("{} - {}\n".format(k, v))
