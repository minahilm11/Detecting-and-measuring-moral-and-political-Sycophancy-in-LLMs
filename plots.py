import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np
import math

all_topics = False
identity_pairs = [("liberals", "conservatives"),("collectivists", "individualists"),("environmentalists", "industrialists"),
                  ("socialists", "capitalists"),("secularists","theocrats"),
                  ("care_harm","authority_subversion"),("fairness_cheating","loyalty_betrayal")]
#identityA, identityB = identity_pairs[0]
def get_data_for_model(model,identityA,identityB):
    model_path = "gpt_4/" if model == "gpt-4" else "gpt_3_5/"

    folder = model_path + identityA + "_" + identityB + "/"
    # get topics from file names in folder
    topics = []
    data = {}
    def logprob_to_percent(logprob):
        return math.exp(logprob)*100
    for filename in os.listdir(model_path + identityA + "_" + identityB):
        identityA=identityA.replace("_","/")
        identityB=identityB.replace("_","/")
        if "rated" in filename:
            topic=filename.split("_rated")[0]
            topics.append(topic)
            with open(folder + filename, 'r', encoding='utf-8') as file:
                data[topic]= {}
                data[topic][identityA + "_agree"] = []
                data[topic][identityA + "_disagree"] = []
                data[topic][identityB + "_agree"] = []
                data[topic][identityB + "_disagree"] = []
                data[topic]["empty_" + identityA] = []
                data[topic]["empty_" + identityB] = []
                for line in file:
                    d = json.loads(line)
                    data[topic][identityA + "_agree"].append(logprob_to_percent(float(d[identityA+ "_agree"])))
                    data[topic][identityA + "_disagree"].append(100-logprob_to_percent(float(d[identityA+ "_agree"])))
                    data[topic][identityB + "_agree"].append(logprob_to_percent(float(d[identityB+ "_agree"])))
                    data[topic][identityB + "_disagree"].append(100-logprob_to_percent(float(d[identityB+ "_agree"])))
                    e1= logprob_to_percent(float(d["empty_" + identityA]))
                    e2= logprob_to_percent(float(d["empty_" + identityB]))
                    e1=100*e1/(e1+e2)
                    e2=100-e1
                    data[topic]["empty_" + identityA].append(e1)
                    data[topic]["empty_" + identityB].append(e2)
    return data
       

def get_avg(data,identityA,identityB):
        averages = {
            identityA + "_agree": np.mean([np.mean(data[topic][identityA + "_agree"]) for topic in data]),
            identityA + "_disagree": np.mean([np.mean(data[topic][identityA + "_disagree"]) for topic in data]),
            identityB + "_agree": np.mean([np.mean(data[topic][identityB + "_agree"]) for topic in data]),
            identityB + "_disagree": np.mean([np.mean(data[topic][identityB + "_disagree"]) for topic in data]),
            "empty_" + identityA: np.mean([np.mean(data[topic]["empty_" + identityA]) for topic in data]),
            "empty_" + identityB: np.mean([np.mean(data[topic]["empty_" + identityB]) for topic in data]),
        }
        return averages
for identityA, identityB in identity_pairs:
    gpt3_5_data= get_data_for_model("gpt-3.5",identityA,identityB)
    gpt4_data= get_data_for_model("gpt-4",identityA,identityB)
    identityA=identityA.replace("_","/")
    identityB=identityB.replace("_","/")
    averages_gpt3_5=get_avg(gpt3_5_data,identityA,identityB)
    averages_gpt4=get_avg(gpt4_data,identityA,identityB)
    

    if all_topics:
        for topic in topics:  # plot each topic
            # barplot with all agreement levels
            plt.figure(figsize=(16, 10))
            o1 = [np.mean(data[topic][identityA + "_agree"]),  np.mean(data[topic][identityB + "_disagree"]), np.mean(data[topic]["empty_"+identityA])]
            o2 = [np.mean(data[topic][identityA + "_disagree"]), np.mean(data[topic][identityB + "_agree"]),np.mean(data[topic]["empty_"+identityB])]
            bar1 = plt.bar([identityA, identityB,"empty"], o1, label=identityA)
            bar2 = plt.bar([identityA, identityB,"empty"], o2, bottom=o1, label=identityB)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.ylabel("Agreement level (%)", fontsize=14)
            plt.title(f"Agreement levels for {topic}", fontsize=16)
            plt.legend()
            plt.show()

    # average for all topics

    plt.figure(figsize=(20, 10))
    categories = [identityA + " bio gpt-3.5", 
                identityA + " bio gpt-4",
                identityB + " bio gpt-3.5",
                identityB + " bio gpt-4",
                "No bio gpt-3.5",
                "No bio gpt-4"]
    o1 = [averages_gpt3_5[identityA + "_agree"],
        averages_gpt4[identityA + "_agree"],
        averages_gpt3_5[identityB + "_disagree"],
        averages_gpt4[identityB + "_disagree"],
        averages_gpt3_5["empty_" + identityA],
        averages_gpt4["empty_" + identityA]]
    o2 = [averages_gpt3_5[identityA + "_disagree"],
          averages_gpt4[identityA + "_disagree"], 
          averages_gpt3_5[identityB + "_agree"],
          averages_gpt4[identityB + "_agree"], 
          averages_gpt3_5["empty_" + identityB],
          averages_gpt4["empty_" + identityB]]

    bar1 = plt.bar(categories, o1, label=identityA)
    bar2 = plt.bar(categories, o2, bottom=o1, label=identityB)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel("Agreement level (%)", fontsize=14)
    plt.title("Average Agreement Levels Across All Topics " + identityA + " " + identityB, fontsize=16)
    plt.legend()
    plt.show()








    

    
    


            
            