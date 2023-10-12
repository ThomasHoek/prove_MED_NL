import argparse
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract annotations from Alpino xml trees"
    )

    # Arguments covering directories and files
    parser.add_argument("tsv", metavar="tsv", help="path to the original MED_NL tsv")
    parser.add_argument(
        "alpino", metavar="DIR", help="path to create the alpino raw file"
    )
    parser.add_argument("sen_pl", metavar="DIR", help="path to crease sen_pl")

    # pre-processing arguments
    args = parser.parse_args()
    return args


##############################################################################
################################ Main function ################################
if __name__ == "__main__":
    args = parse_arguments()

    med_NL = f"{args.tsv}"
    output_file = open(f"{args.alpino}", "w+")
    prolog_file = open(f"{args.sen_pl}", "w+")

    # make sent.pl
    sents: set[str] = set()
    with open(med_NL) as TSV:
        for row in csv.DictReader(TSV, delimiter="\t"):
            sents.update([row["sentence1"], row["sentence2"]])

    sort_dict = {}
    for counter, i in enumerate(sorted(sents), start=1):
        output_file.writelines(i)
        output_file.writelines("\n\n")
        sort_dict[i] = counter

    dict_label = {"entailment": "yes", "neutral": "unknown"}

    with open(med_NL) as tsv:
        for row in csv.DictReader(tsv, delimiter="\t"):
            clean_sent1 = row["sentence1"].replace(r"'", r"\'")
            clean_sent2 = row["sentence2"].replace(r"'", r"\'")

            prolog_file.write(f"%problem id = {row['index']}\n")
            prolog_file.write(
                f"sen_id({sort_dict[row['sentence1']]}, {row['index']}, 'p', '{row['genre'][:5]}', '{dict_label[row['gold_label']]}', '{clean_sent1}').\n"
            )
            prolog_file.write(
                f"sen_id({sort_dict[row['sentence2']]}, {row['index']}, 'h', '{row['genre'][:5]}', '{dict_label[row['gold_label']]}', '{clean_sent2}').\n"
            )

    print("Please manually comment broken files; see MED_NL/problems/sen_pl_sen.txt on github if reproducing")
