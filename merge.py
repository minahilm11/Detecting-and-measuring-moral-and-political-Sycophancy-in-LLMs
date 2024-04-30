import os
import json
import pandas as pd
import math
data = []
def logprob_to_percent(logprob):
        return math.exp(logprob) * 100
for model in ["gpt_3_5","gpt_4"]:
    for id_A,id_B in [("liberals", "conservatives"), ("collectivists", "individualists"), ("environmentalists", "industrialists"),
                  ("socialists", "capitalists"), ("secularists", "theocrats"),
                  ("care_harm", "authority_subversion"), ("fairness_cheating", "loyalty_betrayal")]:
        topics = []
        for filename in os.listdir(model + "/" + id_A + "_" + id_B):
           topics.append(filename.split("_rated")[0]) 
        
        for topic in topics:
            with open(model + "/" + id_A + "_" + id_B + "/" + topic + "_rated.jsonl", 'r', encoding='utf-8') as file:
                identityA = id_A.replace("_", "/")
                identityB = id_B.replace("_", "/")
                for line in file:
                    d = json.loads(line)
                    new_d = {}
                    new_d["question"] = d["question"]
                    new_d["option_A"] = d["option_" + identityA]
                    new_d["option_B"] = d["option_" + identityB]
                    new_d["agree_A"] = d[identityA + "_agree"]
                    new_d["agree_B"] = d[identityB + "_agree"]
                    new_d["empty_A"] = d["empty_" + identityA]
                    new_d["empty_B"] = d["empty_" + identityB]
                    new_d["disagree_A"] = math.log(1 - math.exp(new_d["agree_A"])) if 1 - math.exp(new_d["agree_A"]) > 0 else -100
                    new_d["disagree_B"] = math.log(1 - math.exp(new_d["agree_B"])) if 1 - math.exp(new_d["agree_B"]) > 0 else -100



                    new_d["model"] = model
                    new_d["identityA"] = id_A
                    new_d["identityB"] = id_B
                    new_d["topic"] = topic

                    data.append(new_d)
print(data[0])
df = pd.DataFrame(data)
print(df.head())
# save the data to a csv file
df.to_csv("merged_data.csv", index=False)

                