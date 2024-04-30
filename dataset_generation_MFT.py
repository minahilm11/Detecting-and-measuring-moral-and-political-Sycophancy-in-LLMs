import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from google.cloud import aiplatform
from vertexai import preview
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part
from tqdm import tqdm
import os

def chat_text_example(project_id: str, location: str,topic) -> str:
    vertexai.init(project=project_id, location=location)
    prompt_variables = {
        "MORAL_FOUNDATION_A": "liberty/oppression",
        "MORAL_FOUNDATION_B": "loyalty/betrayal",
        "Topic": topic,
    }
    split1 = prompt_variables["MORAL_FOUNDATION_A"].split("/")
    split2 = prompt_variables["MORAL_FOUNDATION_B"].split("/")
    MF_path = split1[0]+"_"+split1[1]+"_" + split2[0] + "_" + split2[1]
    with open("examples_" + MF_path + ".txt", "r") as example_file, open("example_prompt_" + MF_path + ".txt", "r") as prompt_file:
        examples = example_file.read()
        example_prompt = prompt_file.read()
        prompt_variables["Examples"] = examples
        prompt_variables["example_prompt"] = example_prompt
  
    
    with open("prompt_MF.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.format(**prompt_variables)
    
    model = GenerativeModel("gemini-1.0-pro")
    config = {
        "max_output_tokens": 2048,
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 32
    }
    
    def get_chat_response(prompt: str) -> str:
        chat = model.start_chat(history=[
            Content(role="user", parts=[Part.from_text(prompt_variables["example_prompt"])]),
            Content(role="model", parts=[Part.from_text(prompt_variables["Examples"])])
        ])
        response = chat.send_message(prompt, generation_config=config)
        return response.text
    
    os.makedirs(MF_path, exist_ok=True)
    with open(MF_path + "/"+ prompt_variables["Topic"] +".json", "a", encoding="utf-8") as f:
        for i in tqdm(range(42)):
            try:
                response = get_chat_response(prompt)
            except Exception as e:
                print(e)
                continue

            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.replace("[", "")
            response = response.replace("]", "")
            response += ",\n"
            f.write(response)

for topic in [ "Technology and surveillance", "Law and Order", "Healthcare", "Climate Change", "Globalization","Defense and Military", 
              "Economic Policies","Immigration","Social Equality and Rights","Media Freedom"]:
    chat_text_example("master-thesis-project-415713", "europe-west4",topic)
                      