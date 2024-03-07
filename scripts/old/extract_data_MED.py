import argparse
import spacy
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract annotations from Alpino xml trees"
    )

    # Arguments covering directories and files
    parser.add_argument("tsv", metavar="tsv", help="path to the original MED tsv")
    parser.add_argument(
        "out_folder", metavar="output folder", help="folder to output data to"
    )

    # pre-processing arguments
    args = parser.parse_args()
    return args


replace_dict: dict[str, str] = {
    "aren't": "are not",
    "can't": "can not",
    "couldn't": "could not",
    "Don't": "Do not",
    "don't": "do not",
    "didn't": "did not",
    "doesn't": "does not",
    "hasn't": "has not",
    "Hamletwasn't": "Hamletwas not",
    "haven't": "have not",
    "isn't": "is not",
    "mustn't": "must not",
    "needn't": "need not",
    "shouldn't": "should not",
    "wasn't": "was not",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
    "Wouldn't": "Would not"
}

replace_dict2 = {
    r"'s": r"\'s",
    r"'m": r"\'m"
}

##############################################################################
################################ Main function ###############################

if __name__ == "__main__":
    args = parse_arguments()

    med_NL = f"{args.tsv}"
    crowd_spl = open(f"{args.out_folder}/crowd.spl", "w+")
    paper_spl = open(f"{args.out_folder}/paper.spl", "w+")
    crowd_sp = open(f"{args.out_folder}/crowd_sen.pl", "w+")
    paper_sp = open(f"{args.out_folder}/paper_sen.pl", "w+")

    tokenizer = spacy.load("en_core_web_sm")

    # make sent.pl
    sents: set[str] = set()
    with open(med_NL) as TSV:
        for row in csv.DictReader(TSV, delimiter="\t"):

            sen1 = ' '.join([replace_dict.get(i, i) for i in row["sentence1"].split()])
            sen2 = ' '.join([replace_dict.get(i, i) for i in row["sentence2"].split()])

            if "n't" in sen1 or "n't" in sen2:
                print(row["sentence1"].split())
                print(row["sentence2"].split())
                print(sen1)
                print(sen2)
                TSV.close()
                raise NotImplementedError("Word not in replace dict")
            clean_sent1 = " ".join([t.text.strip() for t in tokenizer(sen1)])
            clean_sent2 = " ".join([t.text.strip() for t in tokenizer(sen2)])

            for key, value in replace_dict2.items():
                clean_sent1 = clean_sent1.replace(key, value)
                clean_sent2 = clean_sent2.replace(key, value)

            sents.update([clean_sent1, clean_sent2])
    sort_dict = {}
    for counter, i in enumerate(sorted(sents), start=1):
        for out_file in [crowd_spl, paper_spl]:
            out_file.writelines(i)
            out_file.writelines("\n")
        sort_dict[i] = counter

    dict_label = {"entailment": "yes", "neutral": "unknown"}

    with open(med_NL) as tsv:
        for row in csv.DictReader(tsv, delimiter="\t"):

            sen1 = ' '.join([replace_dict.get(i, i) for i in row["sentence1"].split()])
            sen2 = ' '.join([replace_dict.get(i, i) for i in row["sentence2"].split()])

            clean_sent1 = " ".join([t.text.strip() for t in tokenizer(sen1)])
            clean_sent2 = " ".join([t.text.strip() for t in tokenizer(sen2)])

            for key, value in replace_dict2.items():
                clean_sent1 = clean_sent1.replace(key, value)
                clean_sent2 = clean_sent2.replace(key, value)

            out_file = crowd_sp if row["genre"][:5] == "crowd" else paper_sp

            out_file.write(f"%problem id = {row['index']}\n")
            out_file.write(
                f"sen_id({sort_dict[clean_sent1]}, {row['index']}, 'p','{dict_label[row['gold_label']]}', '{clean_sent1}').\n"
            )
            out_file.write(
                f"sen_id({sort_dict[clean_sent2]}, {row['index']}, 'h', '{dict_label[row['gold_label']]}', '{clean_sent2}').\n"
            )
