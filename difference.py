import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np
import math

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
diffs = []
ids = []
ratios = []
for identityA, identityB in identity_pairs:

    gpt3_5_data= get_data_for_model("gpt-3.5",identityA,identityB)
    gpt4_data= get_data_for_model("gpt-4",identityA,identityB)
    identityA=identityA.replace("_","/")
    identityB=identityB.replace("_","/")
    averages_gpt3_5=get_avg(gpt3_5_data,identityA,identityB)
    averages_gpt4=get_avg(gpt4_data,identityA,identityB)

    ratio_A = averages_gpt4[identityA + "_agree"] / averages_gpt4["empty_" + identityA]
    ratio_B = averages_gpt4[identityB + "_agree"] / averages_gpt4["empty_" + identityB]

    
    aboslute_diff_A = averages_gpt4[identityA + "_agree"] - averages_gpt4["empty_" + identityA]
    aboslute_diff_B = averages_gpt4[identityB + "_agree"] - averages_gpt4["empty_" + identityB]
    print(f"{identityA} ratio: {ratio_A}")
    print(f"{identityB} ratio: {ratio_B}")
    print(f"{identityA} absolute difference: {aboslute_diff_A}")
    print(f"{identityB} absolute difference: {aboslute_diff_B}")
    ids.append(identityA)
    ids.append(identityB)
    diffs.append(aboslute_diff_A)
    diffs.append(aboslute_diff_B)
    ratios.append(ratio_A)
    ratios.append(ratio_B)

# plotting the results 
salmon_color = "#FA8072"  # HTML color code for salmon

plt.figure(figsize=(16, 8))
plt.rcParams['font.family'] = 'Times New Roman'
bar1 = plt.bar(ids,diffs, color=salmon_color)
plt.yticks(fontsize=14)
plt.ylabel("Increased agreement\n(Percentage points)", fontsize=14)
plt.title("Absolute increase in agreement based on bio", fontsize=16) 
plt.xticks(fontsize=12, rotation=30)
plt.gca().yaxis.grid(True)
plt.gca().spines['right'].set_visible(False) 
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.show()

plt.figure(figsize=(20, 12))
bar2 = plt.bar(ids,ratios, color=salmon_color)
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel("Increased agreement (ratio)", fontsize=14)
plt.title("Ratio between agreement based on bio compared to no bio ", fontsize=16)
plt.legend()
plt.show()