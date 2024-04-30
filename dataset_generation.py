import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from google.cloud import aiplatform
from vertexai import preview
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part

from tqdm import tqdm
import os



def chat_text_example(project_id: str, location: str,topic:str) -> str:
    vertexai.init(project=project_id, location=location)

    prompt_variables = {
    "Group A": "authoritarians",
    "Group B": "libertarians",
    "Topic": topic,
    }


    with open("examples_" + prompt_variables["Group A"] + "_" + prompt_variables["Group B"] + ".txt", "r") as f, open("example_prompt_" + prompt_variables["Group A"] + "_" + prompt_variables["Group B"] + ".txt", "r") as f2:
        examples = f.read()
        example_prompt = f2.read()
        prompt_variables["Examples"] = examples
        prompt_variables["example_prompt"] = example_prompt
    with open("prompt.txt", "r") as f:
        prompt = f.read()
    prompt = prompt.format(**prompt_variables)
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    
    config = {"max_output_tokens": 2048, "temperature": 0.9, "top_p": 1, "top_k": 32}
    
    def get_chat_response(prompt: str) -> str:
        chat = model.start_chat(history=[Content(role="user", parts=[Part.from_text(prompt_variables["example_prompt"])]),
                                        Content(role="model", parts=[Part.from_text(prompt_variables["Examples"])])])
        response = chat.send_message(prompt, generation_config=config)
        return response.text
        
    os.makedirs(prompt_variables["Group A"]+"_"+prompt_variables["Group B"], exist_ok=True)
    with open(prompt_variables["Group A"]+"_"+prompt_variables["Group B"] + "/"+ prompt_variables["Topic"] +".json", "a", encoding="utf-8") as f:
        for i in tqdm(range(42)):
            try:
                response = get_chat_response(prompt)
                response=response.replace("```json","")
                response=response.replace("```","")
                response=response.replace("[","")
                response=response.replace("]","")
                response += ",\n"
                f.write(response)
            except Exception as e:
                print(e)
                continue
            
    #"Technology and surveillance", "Law and Order",
    #"Healthcare", "Climate Change", "Globalization",
for topic in [ "Technology and surveillance", "Law and Order", "Healthcare", "Climate Change", "Globalization","Defense and Military", 
              "Economic Policies","Immigration","Social Equality and Rights","Media Freedom"]:
    chat_text_example("master-thesis-project-415713", "us-central1",topic)
                      #"europe-west4",topic)