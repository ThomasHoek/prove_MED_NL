from collections import defaultdict
import csv

from torch import orgqr


sentences = open("HELP_NL/raw.spl", "r").readlines()


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)

    return ((key, locs) for key, locs in tally.items() if len(locs) > 1)


duplicates = open("scripts/help/duplicates.txt", "w+")
ant = sorted(list_duplicates(sentences))
for dup, num in ant:
    duplicates.writelines(f"{dup.rstrip()} | {str(num)}\n")


# -----------------------


def duplicate_check(sen1, sen2):
    return sen1 in duplicate_list or sen2 in duplicate_list


help_tsv = "HELP_NL/pmb_train_v1.0.tsv"
HELP_NL = "HELP_NL/other/help_nl_self_select_nl.txt"
HELP_EN = "HELP_NL/other/help_nl_self_select.txt"
prolog_file = open("HELP_NL/sen.pl", "w+")

dutch_sent: list[str] = [x.rstrip() for x in open(HELP_NL, "r").readlines()]
english_sent: list[str] = [x.rstrip() for x in open(HELP_EN, "r").readlines()]
english_number_dict = dict(zip(english_sent, range(len(english_sent))))
english_dutch_dict = dict(zip(english_sent, dutch_sent))

duplicate_list = [x[0].rstrip() for x in sorted(list_duplicates(dutch_sent))]
dict_label = {"entailment": "yes", "neutral": "unknown"}


counter = 1
with open(help_tsv) as TSV:
    for row in csv.DictReader(TSV, delimiter="\t"):
        org = row["ori_sentence"].rstrip()
        new = row["new_sentence"].rstrip()

        
        if org in english_sent:
            dutch_org = english_dutch_dict[org].replace(r"'", r"\'")
            dutch_new = english_dutch_dict[new].replace(r"'", r"\'")
            org_idx = english_number_dict[org]
            new_idx = english_number_dict[new]

            if not duplicate_check(dutch_org, dutch_new):
                # print(dutch_org)
                # print(dutch_new)
                
                # continue

                prolog_file.write(f"%problem id = {counter}\n")
                prolog_file.write(
                    f"sen_id({new_idx}, {counter}, 'p', 'HELP', '{dict_label[row['gold_label']]}', '{dutch_org}').\n"
                )

                prolog_file.write(
                    f"sen_id({new_idx}, {counter}, 'h', 'HELP', '{dict_label[row['gold_label']]}', '{dutch_new}').\n"
                )
                counter += 1
