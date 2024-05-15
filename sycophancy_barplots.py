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
                ("socialists", "capitalists"), ("secularists", "theocrats"), ("authoritarians", "libertarians"), ("progressives", "traditionalists"),
                ("care_harm", "authority_subversion"), ("care_harm", "loyalty_betrayal"), ("care_harm", "sanctity_degradation"),
                ("fairness_cheating", "authority_subversion"), ("fairness_cheating", "loyalty_betrayal"), ("fairness_cheating", "sanctity_degradation"),
                ("liberty_oppression", "authority_subversion"), ("liberty_oppression", "loyalty_betrayal"), ("liberty_oppression", "sanctity_degradation")]
                                                          
def get_data_for_model(model,identityA,identityB):
    model_path = "data_gpt_4/" if model == "gpt-4" else "data_gpt_3_5/"
    folder = model_path + identityA + "_" + identityB + "/"
    topics = []
    data = {}
    def logprob_to_percent(logprob):
        return math.exp(logprob) * 100
    for filename in os.listdir(model_path + identityA + "_" + identityB):
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


# Calculate the average agreement levels for each identity pair
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
    averages_gpt3_5=get_avg(gpt3_5_data,identityA,identityB)
    averages_gpt4=get_avg(gpt4_data,identityA,identityB)




    # Plot average agreement levels across all topics
    fig, ax = plt.subplots(figsize=(20, 10))
    categories = ["GPT-3.5", "GPT-4", "GPT-3.5", "GPT-4", "GPT-3.5", "GPT-4"]
    width = 0.5
    scale = 0.8
    x = [x*scale if x%2==0 else x*scale+1/2-scale for x in range(len(categories))]

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

    bar1 = ax.bar(x, o1, label="Agrees with " + identityA, color='skyblue', width=width, edgecolor="black", linewidth=1.5)
    bar2 = ax.bar(x, o2, bottom=o1, label="Agrees with " + identityB, color='salmon', width=width, edgecolor="black", linewidth=1.5)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14, fontname="Times New Roman")
    group_labels = ["Bio for " + identityA, "Bio for " + identityB, 'Empty Bio']
    group_positions = [2*x*scale+width/2 for x in range(len(group_labels))]

    for label, pos in zip(group_labels, group_positions):
        ax.text(pos, -8, label, ha='center', fontsize=16, fontname="Times New Roman", fontweight='bold')

    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_yticklabels(np.arange(0, 101, 10), fontsize=14, fontname="Times New Roman")
    ax.set_ylabel("Agreement Level (Percentage %)", fontsize=14, fontname="Times New Roman")
    ax.set_title("Average Agreement Levels Across All Topics for " + identityA + " vs " + identityB,
                    fontsize=16, fontname="Times New Roman", fontweight="bold")
    ax.legend(fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.tight_layout()
    plt.savefig("Visualisations/avg_agreement_" + identityA + "_" + identityB + ".png", dpi=300)
    plt.show()