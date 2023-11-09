import csv
import numpy as np
from sklearn.metrics import classification_report

data = open("Results/MED_NL/crowd/alpino_aethel.alpino.ans", "r").readlines()
data = [x.rstrip().split("\t") for x in data[3:]]

data_dict = {}
for line in data:
    data_dict[line[0]] = line[1].lower()

data = open("Results/MED_NL/paper/alpino_aethel.alpino.ans", "r").readlines()
data = [x.rstrip().split("\t") for x in data[3:]]
for line in data:
    data_dict[line[0]] = line[1].lower()


feature_set = set()
med_NL = "MED_NL/MED_NL.tsv"
med_info_dict = {}
with open(med_NL) as TSV:
    for row in csv.DictReader(TSV, delimiter="\t"):
        features = row["genre"].split(":")
        features = [x.lower() for x in features]
        feature_set.update(features)
        med_info_dict[row["index"]] = (row["gold_label"].lower(), features)


import sys

sys.stdout = open("Results/MED_NL/confusion_matrix.txt", "w")
for feature in feature_set:
    true_data = []
    predictions = []

    for number in med_info_dict.keys():
        if feature in med_info_dict[number][1]:
            true_data.append(med_info_dict[number][0])
            if number in data_dict:
                predictions.append(data_dict[number])
            else:
                predictions.append("neutral")

    # if len(predictions) > 10:
    print(feature)
    print(classification_report(true_data, predictions, digits=3, zero_division=np.nan))
# sys.stdout.close()


sys.stdout = open("Results/MED_NL/confusion_matrix2.txt", "w")

feature_lst = [
    "lexical_knowledge",
    "conjunction",
    "disjunction",
    "conditionals",
    "npi",
    "reverse",
    "other",
]
for second_feature in ["upward_monotone", "downward_monotone"]:
    for feature in feature_lst:
        true_data = []
        predictions = []
        for number in med_info_dict.keys():
            if feature == "other":
                if (
                    len(set(feature_lst).intersection(set(med_info_dict[number][1])))
                    == 0
                    and second_feature in med_info_dict[number][1]
                ):
                    true_data.append(med_info_dict[number][0])
                    if number in data_dict:
                        predictions.append(data_dict[number])
                    else:
                        predictions.append("neutral")

            else:
                if (
                    feature in med_info_dict[number][1]
                    and second_feature in med_info_dict[number][1]
                ):
                    true_data.append(med_info_dict[number][0])
                    if number in data_dict:
                        predictions.append(data_dict[number])
                    else:
                        predictions.append("neutral")

        if len(predictions) > 1:
            print(feature, second_feature)
            print(
                classification_report(
                    true_data, predictions, digits=4, zero_division=np.nan
                )
            )

feature_lst = ["lexical_knowledge", "disjunction", "npi", "other"]
second_feature = "non_monotone"
for feature in feature_lst:
    true_data = []
    predictions = []
    for number in med_info_dict.keys():
        if feature == "other":
            if (
                len(set(feature_lst).intersection(set(med_info_dict[number][1]))) == 0
                and second_feature in med_info_dict[number][1]
            ):
                true_data.append(med_info_dict[number][0])
                if number in data_dict:
                    predictions.append(data_dict[number])
                else:
                    predictions.append("neutral")

        else:
            if (
                feature in med_info_dict[number][1]
                and second_feature in med_info_dict[number][1]
            ):
                true_data.append(med_info_dict[number][0])
                if number in data_dict:
                    predictions.append(data_dict[number])
                else:
                    predictions.append("neutral")

    if len(predictions) > 1:
        print(feature, second_feature)
        print(
            classification_report(
                true_data, predictions, digits=4, zero_division=np.nan
            )
        )
sys.stdout.close()
