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

# A list of tuples, each containing a pair of our identities
identity_pairs = [
    ("liberals", "conservatives"),
    ("collectivists", "individualists"),
    ("environmentalists", "industrialists"),
    ("socialists", "capitalists"),
    ("secularists", "theocrats"),
    ("care_harm", "authority_subversion"),
    ("fairness_cheating", "loyalty_betrayal")
]

# A function designed to extract and transform data related to different identity pairs for a given model.
def get_data_for_model(model, identityA, identityB):
    # Ternary operation to determine the folder path based on the model type (GPT-3.5 or GPT-4).
    model_path = "gpt_4/" if model == "gpt-4" else "gpt_3_5/"
    
    # Constructs the path to the data folder using the model path and the identities.
    folder = model_path + identityA + "_" + identityB + "/"
    
    # Initializes an empty list for topics and a dictionary to hold the data.
    topics = []
    data = {}

    # A nested function that converts log probabilities to percentages. 
    def logprob_to_percent(logprob):
        return math.exp(logprob) * 100

    # Iterates over each file in the directory corresponding to the identity pair.
    for filename in os.listdir(model_path + identityA + "_" + identityB):
        # Replaces underscores with slashes in identity names, probably for formatting purposes.
        identityA = identityA.replace("_", "/")
        identityB = identityB.replace("_", "/")
        
        # Checks if the current file is a rated data file for the topic.
        if "rated" in filename:
            # Extracts the topic name from the filename.
            topic = filename.split("_rated")[0]
            # Appends the topic name to the topics list.
            topics.append(topic)
            
            # Opens the rated data file for reading.
            with open(folder + filename, 'r', encoding='utf-8') as file:
                # Initializes the data structure for this topic.
                data[topic] = {}
                data[topic][identityA + "_agree"] = []
                data[topic][identityA + "_disagree"] = []
                data[topic][identityB + "_agree"] = []
                data[topic][identityB + "_disagree"] = []
                data[topic]["empty_" + identityA] = []
                data[topic]["empty_" + identityB] = []

                # Reads each line of the file (assumed to be a JSON string).
                for line in file:
                    # Converts the JSON string to a dictionary.
                    d = json.loads(line)
                    
                    # Processes and appends the agreement/disagreement data for both identities.
                    # The data transformation uses the nested logprob_to_percent function.
                    data[topic][identityA + "_agree"].append(logprob_to_percent(float(d[identityA + "_agree"])))
                    data[topic][identityA + "_disagree"].append(100 - logprob_to_percent(float(d[identityA + "_agree"])))
                    data[topic][identityB + "_agree"].append(logprob_to_percent(float(d[identityB + "_agree"])))
                    data[topic][identityB + "_disagree"].append(100 - logprob_to_percent(float(d[identityB + "_agree"])))
                    # Calculates the percentage for an "empty" bio category, which might be a baseline or control.
                    e1 = logprob_to_percent(float(d["empty_" + identityA]))
                    e2 = logprob_to_percent(float(d["empty_" + identityB]))
                    e1 = 100 * e1 / (e1 + e2)
                    e2 = 100 - e1
                    data[topic]["empty_" + identityA].append(e1)
                    data[topic]["empty_" + identityB].append(e2)
    return data, topics # return topics as well (new addition)

#fix below to keep the agreement level 100
for identityA, identityB in identity_pairs:
    gpt3_5_data, topics = get_data_for_model("gpt-3.5", identityA, identityB)
    gpt4_data, _ = get_data_for_model("gpt-4", identityA, identityB)

    identityA = identityA.replace("_", "/")
    identityB = identityB.replace("_", "/")

    plt.figure(figsize=(18, 10))
    width = 0.35 
    x = np.arange(len(topics))

    for model, data, color_A,color_B in [("GPT-3.5", gpt3_5_data, "#1f77b4","#ff7f0e"), ("GPT-4", gpt4_data,"#1f2db4" ,"#c15a00")]:
        agreement_scores_A = [np.mean(data[topic][identityA + "_agree"]) for topic in topics]
        disagreement_scores_A = [np.mean(data[topic][identityA + "_disagree"]) for topic in topics]
        agreement_scores_B = [np.mean(data[topic][identityB + "_agree"]) for topic in topics]
        disagreement_scores_B = [np.mean(data[topic][identityB + "_disagree"]) for topic in topics]
        
        plt.bar(3*x - width/2 if model == "GPT-3.5" else 3*x + width/2, agreement_scores_A, width, label=f"{identityA} Agree ({model})",color=color_A)
        plt.bar(3*x - width/2 if model == "GPT-3.5" else 3*x + width/2, disagreement_scores_A, width, bottom=agreement_scores_A, label=f"{identityA} Disagree ({model})",color=color_B)
        
        plt.bar(3*x+1+ width/2 if model == "GPT-3.5" else 3*x+1 - width/2, disagreement_scores_B, width, label=f"{identityB} Agree ({model})",color=color_A)
        plt.bar(3*x+1 + width/2 if model == "GPT-3.5" else 3*x+1 - width/2, agreement_scores_B, width, bottom=disagreement_scores_B, label=f"{identityB} Disagree ({model})",color=color_B)


    plt.xlabel("Topics", fontsize=16)
    plt.ylabel("Agreement/Disagreement Level (%)", fontsize=16)
    plt.title(f"Sycophancy Levels Across Topics for {identityA} vs {identityB}", fontsize=20)
    plt.xticks(x, topics, rotation=45, ha="right", fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.show()

