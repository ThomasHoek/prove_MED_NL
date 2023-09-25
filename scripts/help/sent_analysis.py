from collections import defaultdict
import csv


def duplicate_check(sen1: str, sen2: str) -> bool:
    # remove duplicate sentences
    return sen1 in duplicate_list or sen2 in duplicate_list


def list_duplicates(seq):
    # taken from stackoverflow:  https://stackoverflow.com/a/5419576
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)

    return ((key, locs) for key, locs in tally.items() if len(locs) > 1)


# find all duplicates and write to seperate file (analysis)
if False:
    duplicates = open("scripts/help/duplicates.txt", "w+")
    sentences = open("HELP_NL/raw.spl", "r").readlines()

    ant = sorted(list_duplicates(sentences))
    for dup, num in ant:
        duplicates.writelines(f"{dup.rstrip()} | {str(num)}\n")


# all files for sen.pl
help_tsv = "HELP_NL/pmb_train_v1.0.tsv"
HELP_NL = "HELP_NL/other/help_nl_self_select_nl.txt"
HELP_EN = "HELP_NL/other/help_nl_self_select.txt"
prolog_file = open("HELP_NL/sen.pl", "w+")

# open and pre-processing
dutch_sent: list[str] = [x.rstrip() for x in open(HELP_NL, "r").readlines()]
english_sent: list[str] = [x.rstrip() for x in open(HELP_EN, "r").readlines()]

# make dictionaries for translating eng to index/dutch
english_number_dict = dict(zip(english_sent, range(1, len(english_sent) + 1)))
english_dutch_dict = dict(zip(english_sent, dutch_sent))
dict_label = {"entailment": "yes", "neutral": "unknown"}

# get all duplicate dutch sentences
duplicate_list: list[str] = [x[0].rstrip() for x in sorted(list_duplicates(dutch_sent))]

# make sen.pl
counter = 1
with open(help_tsv) as TSV:
    # using pmb_train_v1.0.tsv, find english sentence in HELP_EN (hand chosen)
    for row in csv.DictReader(TSV, delimiter="\t"):
        org: str = row["ori_sentence"].rstrip()
        new: str = row["new_sentence"].rstrip()

        # use dictionaries to convert eng -> NL and eng -> index
        if org in english_sent:
            dutch_org: str = english_dutch_dict[org].replace(r"'", r"\'")
            dutch_new: str = english_dutch_dict[new].replace(r"'", r"\'")
            org_idx: int = english_number_dict[org]
            new_idx: int = english_number_dict[new]

            if not duplicate_check(dutch_org, dutch_new):
                prolog_file.write(f"%problem id = {counter}\n")
                prolog_file.write(
                    f"sen_id({org_idx}, {counter}, 'p', 'HELP', '{dict_label[row['gold_label']]}', '{dutch_org}').\n"
                )

                prolog_file.write(
                    f"sen_id({new_idx}, {counter}, 'h', 'HELP', '{dict_label[row['gold_label']]}', '{dutch_new}').\n"
                )
                counter += 1
