import os
import csv

path = os.getcwd() + "/../MED_NL"
med_NL = f"{path}/MED_NL.tsv"
output_file = open(f"{path}/alpino_raw.txt", "w+")
prolog_file = open(f"{path}/sen.pl", "w+")


sents: set[str] = set()
with open(med_NL) as TSV:
    for row in csv.DictReader(TSV, delimiter="\t"):
        sents.update([row["sentence1"], row["sentence2"]])


# TODO org counts on first appearance, test if bugs.
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
