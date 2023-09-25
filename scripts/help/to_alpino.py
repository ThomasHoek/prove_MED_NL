sentences = open("scripts/help/help_nl_self_select_nl.txt", "r")
alpino = open("scripts/help/alpino.txt", "w+")


for i in sentences.readlines():
    alpino.writelines(i)
    alpino.writelines("\n")




