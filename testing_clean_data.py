from openai import OpenAI
import json
from tqdm import tqdm
import math
import random
import os
import re

model = "gpt-3.5-turbo"
identity_pairs = [("liberals", "conservatives"),("collectivists", "individualists"),("environmentalists", "industrialists"),
                  ("socialists", "capitalists"),("secularists","theocrats"),
                  ("authoritarians", "libertarians"),("progressives", "traditionalists"),
                  ("care_harm","authority_subversion"), ("care_harm","sanctity_degradation"), ("care_harm","loyalty_betrayal"),
                  ("fairness_cheating","loyalty_betrayal"),("fairness_cheating","authority_subversion"),("fairness_cheating","sanctity_degradation"),
                    ("liberty_opression","sanctity_degradation"),("liberty_opression","authority_subversion"),("liberty_opression","loyalty_betrayal")]


topics = [
    "Climate Change", "Defense and military", "Economic Policies", "Globalization",
    "Healthcare", "Immigration", "Law and Order", "Media Freedom",
    "Social Equality and Rights", "Technology and surveillance"
]  # Topics as shown in the directory structure

def modify_keys(old_key,id_A,id_B):
    

    new_key = old_key.replace(' ', '_')  # Replace spaces with underscores
    new_key = new_key.replace('/', '_')  # Replace slashes with underscores
    new_key = new_key.lower()            # Convert to lowercase
    if new_key == "profile_" + id_A.split("_")[0]:
        new_key = "profile_" + id_A
    if new_key == "profile_" + id_B.split("_")[0]:
        new_key = "profile_" + id_B
    if new_key == "option_" + id_A.split("_")[0]:
        new_key = "option_" + id_A
    if new_key == "option_" + id_B.split("_")[0]:
        new_key = "option_" + id_B
    return new_key

def fix_json_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        content = file.read().strip()
    
    # Ensure it starts with '[' and ends with ']'
    if not content.startswith('['):
        content = '[' + content
    if not content.endswith(']'):
        content = content + ']'
    content = re.sub(r'",\s*\n\s*\}','"\}', content)
    # Attempt to fix missing commas between dictionaries
    content = content.replace('}{', '},{')
    
    try:
        # Try parsing the JSON to see if it's correctly formatted now
        data = json.loads(content)
        print("JSON parsed successfully!")
        return data
    except json.JSONDecodeError as e:
        # Handle cases where JSON is still not valid
        print(f"Error parsing JSON: {e}")
        return None







for identityA, identityB in identity_pairs:  # Process each identity pair
    print(f"Processing {identityA} vs {identityB}")
    topics = []
    for filename in os.listdir(identityA.replace("/","_") + "_" + identityB.replace("/","_")):
        if filename.endswith(".json"):
            topics.append(filename.split(".")[0])
    folder = identityA.replace("/","_") + "_" + identityB.replace("/","_") + "/"        
    for topic in topics:  # Process each topic
        print(f"Processing {topic}")
        input_filename = folder + topic + ".json"
        f_d = fix_json_format(input_filename)
        if f_d is not None:
            json.dump(f_d, open(input_filename, 'w',encoding='utf-8'), indent=4)

        with open(input_filename, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

            # Process each item in the data list
            for i in tqdm(range(len(data))):
                new_data = {}
                for key, value in data[i].items():
                    new_key = modify_keys(key,identityA,identityB)
                    new_data[new_key] = value
                
                # Update the original dictionary with the modified keys
                data[i] = new_data
            with open(input_filename, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)


            with open(input_filename, "r", encoding='utf-8') as infile:
                data = json.load(infile)

                for i in tqdm(range(len(data))):
                    profileA = data[i]["profile_" + identityA]
                    profileB = data[i]["profile_" + identityB]
                    optionA = data[i]["option_" + identityA]
                    optionB = data[i]["option_" + identityB]
                    question = data[i]["question"]
for model in "gpt_3_5","gpt_4":
    for id_A,id_B in identity_pairs:
        folder = model + "/" + id_A + "_" + id_B
        topics = []
        if os.path.exists(folder):
            for filename in os.listdir(model + "/" + id_A + "_" + id_B):
                topics.append(filename.split("_rated")[0]) 
            for topic in topics:
                with open(model + "/" + id_A + "_" + id_B + "/" + topic + "_rated.jsonl", 'r', encoding='utf-8') as file:
                    for i in tqdm(range(len(data))):
                        new_data = {}
                        for key, value in data[i].items():
                            new_key = modify_keys(key)
                            new_data[new_key] = value
                    
                        # Update the original dictionary with the modified keys
                        data[i] = new_data
                with open(model + "/" + id_A + "_" + id_B + "/" + topic + "_rated.jsonl", 'w', encoding='utf-8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)