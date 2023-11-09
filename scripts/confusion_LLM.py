from sklearn.metrics import classification_report
import re
test = open("Results/MED_NL/LLM/out_pred_entail.txt", "r").readlines()


p_label_data = []
p_sum_data = []
c_label_data = []
c_sum_data = []

label_data = []
sum_data = []
for line in test:        
    data = line.split(" ")
    label = re.search(r"(label=\d)", line)[0]
    
    pred = eval(' '.join(data[-3:])[:-2])
    pred_sum = 1 if sum(pred)/len(pred) >= 0.5 else 0

    label_data.append(int(label[-1]))
    sum_data.append(pred_sum)

    if "paper" in re.search(r"(features=\[(.*?)\])", line)[0]:
        p_label_data.append(int(label[-1]))
        p_sum_data.append(pred_sum)
    else:
        c_label_data.append(int(label[-1]))
        c_sum_data.append(pred_sum)

print("crowd")
print(classification_report(c_label_data, c_sum_data, digits=3))

print("paper")
print(classification_report(p_label_data, p_sum_data, digits=3))


print("all")
print(classification_report(label_data, sum_data, digits=3))