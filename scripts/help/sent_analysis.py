from collections import defaultdict


sentences = open("scripts/help/help_nl_self_select_nl.txt", "r").readlines()

def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

duplicates = open("scripts/help/duplicates.txt", "w+")
ant = sorted(list_duplicates(sentences))
for dup, num in ant:
    duplicates.writelines(f"{dup.rstrip()} | {str(num)}\n")

print(len(ant))