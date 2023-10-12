import argparse
import nltk
from nltk.tokenize import word_tokenize
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract annotations from Alpino xml trees"
    )

    # Arguments covering directories and files
    parser.add_argument("tsv", metavar="tsv", help="path to the original MED_NL tsv")
    parser.add_argument("out_folder", metavar="output folder", help="folder to output data to")

    # pre-processing arguments
    args = parser.parse_args()
    return args


##############################################################################
################################ Main function ################################
if __name__ == "__main__":
    args = parse_arguments()

    med_NL = f"{args.tsv}"
    crowd_spl = open(f'{args.out_folder}/crowd.spl', "w+")
    paper_spl = open(f'{args.out_folder}/paper.spl', "w+")
    crowd_sp = open(f'{args.out_folder}/crowd_sen.pl', "w+")
    paper_sp = open(f'{args.out_folder}/paper_sen.pl', "w+")

    # make sent.pl
    sents: set[str] = set()
    with open(med_NL) as TSV:
        for row in csv.DictReader(TSV, delimiter="\t"):
            sents.update([row["sentence1"], row["sentence2"]])

    sort_dict = {}
    for counter, i in enumerate(sorted(sents), start=1):
        for out_file in [crowd_spl, paper_spl]:
            out_file.writelines(" ".join(word_tokenize(i)))
            out_file.writelines("\n")
        sort_dict[i] = counter

    dict_label = {"entailment": "yes", "neutral": "unknown"}

    with open(med_NL) as tsv:
        for row in csv.DictReader(tsv, delimiter="\t"):
            clean_sent1 = " ".join(word_tokenize(row["sentence1"])).replace(r"'", r"\'")
            clean_sent2 = " ".join(word_tokenize(row["sentence2"])).replace(r"'", r"\'")

            out_file = crowd_sp if row['genre'][:5] == "crowd" else paper_sp

            out_file.write(f"%problem id = {row['index']}\n")
            out_file.write(f"sen_id({sort_dict[row['sentence1']]}, {row['index']}, 'p','{dict_label[row['gold_label']]}', '{clean_sent1}').\n")
            out_file.write(f"sen_id({sort_dict[row['sentence2']]}, {row['index']}, 'h', '{dict_label[row['gold_label']]}', '{clean_sent2}').\n")