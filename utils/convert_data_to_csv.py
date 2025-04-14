''' This script converts the jsonl files to csv files. It saves the data in two formats: one with the log probabilities and one with the probabilities in percentage. 
It saves the data in three separate files: one for the moral foundations and one for the political identities, and one for both'''
import os
import json
import pandas as pd
import math
# List of identity pairs

identiy_pairs = [("liberals", "conservatives"),("collectivists", "individualists"),("environmentalists", "industrialists"),
                ("socialists", "capitalists"),("secularists","theocrats"),
                 ("care_harm","authority_subversion"),("fairness_cheating","loyalty_betrayal"), 
                 ("authoritarians", "libertarians"),("progressives", "traditionalists"),
                 ("liberty_oppression","sanctity_degradation"),("liberty_oppression","authority_subversion"),
                 ("care_harm","sanctity_degradation"),("fairness_cheating","authority_subversion"),
                 ("fairness_cheating","sanctity_degradation"),("care_harm","loyalty_betrayal"),
                 ("liberty_oppression","loyalty_betrayal")]
# Function to convert log probabilities to percentages
def logprob_to_percent(logprob):
        return math.exp(logprob) * 100
data = []
# Process data for each model and identity pair
for model in ["gpt_3_5","gpt_4"]:
    for id_A,id_B in identiy_pairs:
        topics = []
        # Get topic names from file names
        for filename in os.listdir("data_" + model + "/" + id_A + "_" + id_B):
           topics.append(filename.split("_rated")[0]) 
        # Process data for each topic
        for topic in topics:
            with open("data_" + model + "/" + id_A + "_" + id_B + "/" + topic + "_rated.jsonl", 'r', encoding='utf-8') as file:
                for line in file:
                    d = json.loads(line)
                    new_d = {}
                    new_d["question"] = d["question"]
                    # Check if options are in the expected format
                    if "option_" + id_A in d:
                        new_d["option_A"] = d["option_" + id_A]
                        new_d["option_B"] = d["option_" + id_B]
                        new_d["agree_A"] = logprob_to_percent(d[id_A + "_agree"])
                        new_d["agree_B"] = logprob_to_percent(d[id_B + "_agree"])
                        new_d["empty_A"] = logprob_to_percent(d["empty_" + id_A])
                        new_d["empty_B"] = logprob_to_percent(d["empty_" + id_B])
                    else:
                        new_d["option_A"] = d["option_" + id_A.replace("_", "/")]
                        new_d["option_B"] = d["option_" + id_B.replace("_", "/")]
                        new_d["agree_A"] = logprob_to_percent(d[id_A.replace("_", "/") + "_agree"])
                        new_d["agree_B"] = logprob_to_percent(d[id_B.replace("_", "/") + "_agree"])
                        new_d["empty_A"] = logprob_to_percent(d["empty_" + id_A.replace("_", "/")])
                        new_d["empty_B"] = logprob_to_percent(d["empty_" + id_B.replace("_", "/")])

                    # Calculate disagree probabilities
                    new_d["disagree_A"] = 100 - new_d["agree_A"]
                    new_d["disagree_B"] = 100 - new_d["agree_B"]


                    # Add metadata to the data point
                    new_d["model"] = model
                    new_d["identityA"] = id_A
                    new_d["identityB"] = id_B
                    new_d["topic"] = topic

                    data.append(new_d)
# Create a DataFrame from the processed data
df = pd.DataFrame(data)
# save the data to a csv file
df.to_csv("merged_data_percent.csv", index=False)
# Define a list of Moral Foundations Theory (MFT) categories
mft = ["care_harm","sanctity_degradation","fairness_cheating","authority_subversion","loyalty_betrayal", "liberty_oppression"]
# Filter the data based on MFT categories
cond_mft = df['identityA'].isin(mft)
mft_data = df[cond_mft]
pol_data = df[~cond_mft]
# Save MFT and non-MFT data to separate CSV files
mft_data.to_csv("csv_data/mft_data_percent.csv", index=False)
pol_data.to_csv("csv_data/pol_data_percent.csv", index=False)

# Repeat the process to save data with log probabilities
data = []
for model in ["gpt_3_5","gpt_4"]:
    for id_A,id_B in identiy_pairs:
        topics = []
        for filename in os.listdir("data_" + model + "/" + id_A + "_" + id_B):
           topics.append(filename.split("_rated")[0]) 
        
        for topic in topics:
            with open("data_" + model + "/" + id_A + "_" + id_B + "/" + topic + "_rated.jsonl", 'r', encoding='utf-8') as file:
                for line in file:
                    d = json.loads(line)
                    new_d = {}
                    new_d["question"] = d["question"]
                    if "option_" + id_A in d:
                        new_d["option_A"] = d["option_" + id_A]
                        new_d["option_B"] = d["option_" + id_B]
                        new_d["agree_A"] = d[id_A + "_agree"]
                        new_d["agree_B"] = d[id_B + "_agree"]
                        new_d["empty_A"] = d["empty_" + id_A]
                        new_d["empty_B"] = d["empty_" + id_B]
                    else:
                        new_d["option_A"] = d["option_" + id_A.replace("_", "/")]
                        new_d["option_B"] = d["option_" + id_B.replace("_", "/")]
                        new_d["agree_A"] = d[id_A.replace("_", "/") + "_agree"]
                        new_d["agree_B"] = d[id_B.replace("_", "/") + "_agree"]
                        new_d["empty_A"] = d["empty_" + id_A.replace("_", "/")]
                        new_d["empty_B"] = d["empty_" + id_B.replace("_", "/")]



                    new_d["model"] = model
                    new_d["identityA"] = id_A
                    new_d["identityB"] = id_B
                    new_d["topic"] = topic

                    data.append(new_d)
df = pd.DataFrame(data)
df.to_csv("csv_data/merged_data.csv", index=False)
mft = ["care_harm","sanctity_degradation","fairness_cheating","authority_subversion","loyalty_betrayal", "liberty_oppression"]
cond_mft = df['identityA'].isin(mft)
mft_data = df[cond_mft]
pol_data = df[~cond_mft]
mft_data.to_csv("csv_data/mft_data.csv", index=False)
pol_data.to_csv("csv_data/pol_data.csv", index=False)
                