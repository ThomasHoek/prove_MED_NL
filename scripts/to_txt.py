import argparse
import csv

parser = argparse.ArgumentParser(description="Part used to create the context from. Train, Test or Trial.")
parser.add_argument('--MED_path', required=True, metavar='FILES', help='Train, test etc of the dataset')
args = parser.parse_args()
MED_path = args.MED_path

paper = []
crowd = []
with open(f"{MED_path}/MED.tsv") as TSV:
    for row in csv.DictReader(TSV, delimiter="\t"):
        if "paper" in row["genre"]:
            paper.append(row)
        else:
            crowd.append(row)

with open(f"{MED_path}/MED_paper.txt", "w+") as paper_file:
    for line in paper:
        paper_file.write('\t'.join([value for _, value in line.items()]))
        paper_file.write("\n")

with open(f"{MED_path}/MED_crowd.txt", "w+") as crowd_file:
    for line in crowd:
        crowd_file.write('\t'.join([value for _, value in line.items()]))
        crowd_file.write("\n")