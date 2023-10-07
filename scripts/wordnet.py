from typing import IO, Any
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Translates wordnet codes from WNProlog to text files"
    )

    # Arguments covering directories and files
    parser.add_argument(
        "dir", metavar="DIR", help="A directory with wordnet information"
    )
    parser.add_argument(
        "output", metavar="FILE_PATH", help="A directory to write the output to"
    )

    # pre-processing arguments
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    # read files
    wn_s_file: IO[Any] = open(f"{args.dir}/wn_s.pl", encoding="utf-8")
    wn_s: list[str] = [x.rstrip() for x in wn_s_file.readlines()]

    # make and innitialise dictionary
    wn_s_dict: dict[str, str] = dict()
    for x in wn_s:
        # get WN_key
        dict_key = x.split("'")[1]

        # value: WN word (dict_key)
        dict_str = x.split("'")[3] + " (" + str(dict_key) + ")"

        if dict_key not in wn_s_dict:
            # first time found
            wn_s_dict[dict_key] = dict_str
        else:
            # if multiple found, append string
            wn_s_dict[dict_key] += f"; {dict_str}"

    wn_s_file.close()

    # use convert dict to translate all the files
    for i in ["wn_ant", "wn_der", "wn_hyp", "wn_sim"]:
        # read data
        wn_read_file: IO[Any] = open(f"{args.dir}/{i}.pl", encoding="utf-8")
        read_str: list[str] = [x.rstrip() for x in wn_read_file.readlines()]

        # split data to tuple of key1 and key2
        wn_data: list[tuple[str, str]] = [
            (x.split("'")[1], x.split("'")[3]) for x in read_str
        ]
        wn_read_file.close()

        # write data back as TSV
        wn_file_write: IO[Any] = open(
            f"{args.output}/{i}.tsv", encoding="utf-8", mode="w+"
        )
        word1: str
        word2: str
        for line in wn_data:
            word1, word2 = line
            wn_file_write.write(f"{wn_s_dict[word1]}\t{wn_s_dict[word2]}\n")
        wn_file_write.close()
