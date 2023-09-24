from collections import defaultdict


sentences = open("scripts/help/help_nl_self_select_nl.txt", "r").readlines()

def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

duplicates = open("scripts/help/duplicates.txt", "w+")
for dup, num in sorted(list_duplicates(sentences)):
    duplicates.writelines(f"{dup.rstrip()} | {str(num)}\n")
