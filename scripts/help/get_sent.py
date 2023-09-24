import os
import csv

path = os.getcwd()

print(path)
HELP = f"{path}/scripts/help/pmb_train_v1.0.tsv"
output_file = open(f"{path}/scripts/help/help_nl.txt", "w+")

sents: set[str] = set()
with open(HELP) as TSV:
    for row in csv.DictReader(TSV, delimiter="\t"):
        sents.update([row["ori_sentence"], row["new_sentence"]])


# TODO org counts on first appearance, test if bugs.
for counter, i in enumerate(sorted(sents), start=1):
    output_file.writelines(i)
    output_file.writelines("\n")
