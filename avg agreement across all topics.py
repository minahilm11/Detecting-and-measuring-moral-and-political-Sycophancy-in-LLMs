import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np
import math

# Average agreement levels across all topics for each identity pair
# Set the aesthetics for the plots globally
sns.set_theme(style="whitegrid")  # Sets a theme with a white background and grid
plt.rcParams.update({
    "figure.figsize": (12, 8),  # Sets the default figure size
    "axes.titlesize": 20,  # Sets the font size of the title
    "axes.labelsize": 18,  # Sets the font size of the labels
    "xtick.labelsize": 16,  # Sets the font size of the x-tick labels
    "ytick.labelsize": 16,  # Sets the font size of the y-tick labels
    "legend.fontsize": 16,  # Sets the font size of the legend
    "axes.prop_cycle": plt.cycler(color=sns.color_palette("hsv", 8))  # Sets a color cycle for lines
})

all_topics = False
identity_pairs = [("liberals", "conservatives"), ("collectivists", "individualists"), ("environmentalists", "industrialists"),
                  ("socialists", "capitalists"), ("secularists", "theocrats"),
                  ("care_harm", "authority_subversion"), ("fairness_cheating", "loyalty_betrayal")]

def get_data_for_model(model,identityA,identityB):
    model_path = "gpt_4/" if model == "gpt-4" else "gpt_3_5/"
    folder = model_path + identityA + "_" + identityB + "/"
    topics = []
    data = {}
    def logprob_to_percent(logprob):
        return math.exp(logprob) * 100
    for filename in os.listdir(model_path + identityA + "_" + identityB):
        identityA = identityA.replace("_", "/")
        identityB = identityB.replace("_", "/")
        if "rated" in filename:
            topic = filename.split("_rated")[0]
            topics.append(topic)
            with open(folder + filename, 'r', encoding='utf-8') as file:
                data[topic] = {}
                data[topic][identityA + "_agree"] = []
                data[topic][identityA + "_disagree"] = []
                data[topic][identityB + "_agree"] = []
                data[topic][identityB + "_disagree"] = []
                data[topic]["empty_" + identityA] = []
                data[topic]["empty_" + identityB] = []
                for line in file:
                    d = json.loads(line)
                    data[topic][identityA + "_agree"].append(logprob_to_percent(float(d[identityA + "_agree"])))
                    data[topic][identityA + "_disagree"].append(100 - logprob_to_percent(float(d[identityA + "_agree"])))
                    data[topic][identityB + "_agree"].append(logprob_to_percent(float(d[identityB + "_agree"])))
                    data[topic][identityB + "_disagree"].append(100 - logprob_to_percent(float(d[identityB + "_agree"])))
                    e1 = logprob_to_percent(float(d["empty_" + identityA]))
                    e2 = logprob_to_percent(float(d["empty_" + identityB]))
                    e1 = 100 * e1 / (e1 + e2)
                    e2 = 100 - e1
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
            plt.figure(figsize=(16, 10))
            o1 = [np.mean(data[topic][identityA + "_agree"]), np.mean(data[topic][identityB + "_disagree"]), np.mean(data[topic]["empty_" + identityA])]
            o2 = [np.mean(data[topic][identityA + "_disagree"]), np.mean(data[topic][identityB + "_agree"]), np.mean(data[topic]["empty_" + identityB])]
            bar1 = plt.bar([identityA, identityB, "empty"], o1, label=identityA)
            bar2 = plt.bar([identityA, identityB, "empty"], o2, bottom=o1, label=identityB)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.ylabel("Agreement level (%)", fontsize=14)
            plt.title(f"Agreement levels for {topic}", fontsize=16)
            plt.legend()
            plt.show()

    plt.figure(figsize=(20, 10))
    categories = [
    "GPT-3.5",
    "GPT-4",
    "GPT-3.5",
    "GPT-4",
    "GPT-3.5",
    "GPT-4"]    

    width=0.5
    scale=0.8
    x = [ x*scale if x%2==0 else x*scale+1/2-scale for x in range(len(categories))]
    o1 = [averages_gpt3_5[identityA + "_agree"], averages_gpt4[identityA + "_agree"], averages_gpt3_5[identityB + "_disagree"], averages_gpt4[identityB + "_disagree"], averages_gpt3_5["empty_" + identityA], averages_gpt4["empty_" + identityA]]
    o2 = [averages_gpt3_5[identityA + "_disagree"], averages_gpt4[identityA + "_disagree"], averages_gpt3_5[identityB + "_agree"], averages_gpt4[identityB + "_agree"], averages_gpt3_5["empty_" + identityB], averages_gpt4["empty_" + identityB]]
    bar1 = plt.bar(x, o1, label="agrees with " + identityA, color='skyblue',width=width)
    bar2 = plt.bar(x, o2, bottom=o1, label="agrees with " +identityB, color='salmon',width=width)
    plt.xticks(x, categories, fontsize=14)
    group_labels = ["Bio for " + identityA, "Bio for " + identityB, 'Empty Bio']
    group_positions = [2*x*scale+width/2 for x in range(len(group_labels))]

    # Adding text for each group above the bars
    for label, pos in zip(group_labels, group_positions):
        plt.text(pos, -8, label, ha='center', fontsize=16, fontweight='bold')


    plt.yticks(fontsize=14)
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.ylabel("Agreement level (%)", fontsize=14)
    plt.title("Average agreement levels across all topics for " + identityA + " vs " + identityB, fontsize=16)
    plt.legend()
    plt.show()
