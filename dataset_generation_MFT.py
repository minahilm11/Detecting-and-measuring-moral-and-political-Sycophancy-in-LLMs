'''Script to generate dataset for Moral Foundations Theory (MFT) using Vertex AI's Generative Model API. Note that you must have a google cloud project and API key to run this code.'''
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part
from tqdm import tqdm
import os
# Set this to your google cloud project name before running
project_name = ""

def chat_text_example(project_id: str, location: str,topic) -> str:
    # Initialize Vertex AI with the given project ID and location

    vertexai.init(project=project_id, location=location)
    # Define prompt variables. There must be fewshot examples and a specific prompt for the few shot examples for each moral foundation path
    prompt_variables = {
        "MORAL_FOUNDATION_A": "fairness/cheating",
        "MORAL_FOUNDATION_B": "sanctity/degradation",
        "Topic": topic,
    }
    # Split the moral foundation strings and create a file path
    split1 = prompt_variables["MORAL_FOUNDATION_A"].split("/")
    split2 = prompt_variables["MORAL_FOUNDATION_B"].split("/")
    MF_path = split1[0]+"_"+split1[1]+"_" + split2[0] + "_" + split2[1]
    # Read few_shot examples and the specific prompt for the few shot examples from files based on the moral foundation path
    with open("few_shot_examples/examples_" + MF_path + ".txt", "r") as example_file, open("dataset_gen_prompts/example_prompt_" + MF_path + ".txt", "r") as prompt_file:
        examples = example_file.read()
        example_prompt = prompt_file.read()
        prompt_variables["Examples"] = examples
        prompt_variables["example_prompt"] = example_prompt
  
    # Read the main prompt from a file
    with open("prompt_MFT.txt", "r") as f:
        prompt = f.read()
    # Add the prompt variables to the prompt
    prompt = prompt.format(**prompt_variables)

    # Load gemini
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    # Define the model configuration
    config = {
        "max_output_tokens": 2048,
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 32
    }
    
    def get_chat_response(prompt: str) -> str:
        # Start a chat session with the model
        chat = model.start_chat(history=[
            Content(role="user", parts=[Part.from_text(prompt_variables["example_prompt"])]),
            Content(role="model", parts=[Part.from_text(prompt_variables["Examples"])])
        ])
        # Send the prompt to the model and get the response
        response = chat.send_message(prompt, generation_config=config)
        return response.text
    # Create a directory for the dataset if it doesn't exist
    os.makedirs("datasets/" + MF_path, exist_ok=True)
    # Open a file to store the responses

    with open("datasets/" + MF_path + "/"+ prompt_variables["Topic"] +".json", "a", encoding="utf-8") as f:
        # Generate responses for a specified number of iterations this will generate 40*5=200 examples
        for i in tqdm(range(40)):
            try:
                response = get_chat_response(prompt)
            except Exception as e:
                print(e)
                continue
            # Clean up the response by removing specific substrings
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.replace("[", "")
            response = response.replace("]", "")
            response += ",\n"
            # Write the response to the file
            f.write(response)
# List of topics to generate responses for
topics = ["Technology and surveillance", "Law and Order", "Healthcare", "Climate Change", "Globalization","Defense and Military", 
              "Economic Policies","Immigration","Social Equality and Rights","Media Freedom"]
for topic in topics:
    # Generate responses for each topic
    chat_text_example(project_name, "europe-west4",topic)
                      