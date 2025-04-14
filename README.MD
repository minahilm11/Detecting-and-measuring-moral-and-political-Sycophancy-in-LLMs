# Moral and Political Sycophancy in Large Language Models

This repository contains code and data for my Master's thesis project investigating moral and political sycophancy in large language models (LLMs). The thesis analyzes the implications of LLMs exhibiting sycophantic behaviour, where they align their responses to match users' moral and political views, for deliberative democracy. 

## Repository Structure

- `csv_data/`: Directory containing CSV data files used in the analysis 
- `data_gpt_3_5/`: GPT-3.5 model data and outputs
- `data_gpt_4/`: GPT-4 model data and outputs  
- `dataset_gen_prompts/`: Prompts used for generating the sycophancy testing datasets
- `datasets/`: Generated datasets for sycophancy testing
- `few_shot_examples/`: Few-shot learning examples used to prime the models
- `utils/`: Utility scripts for data processing and analysis
- `Visualisations/`: Directory containing generated visualization images
- `dataset_generation_MFT.py`: Generates moral foundations theory dataset for implicit sycophancy testing
- `dataset_generation_political.py`: Generates political identities dataset for explicit sycophancy testing
- `generate_plots.py`: Generates visualizations of sycophancy testing results
- `plots.ipynb`: Jupyter notebook with code for generating other plots and visualizations
- `prompt_MFT.txt`: Text file with prompts for moral foundations testing
- `prompt_political.txt`: Text file with prompts for political identity sycophancy testing  
- `README.MD`: This readme file
- `sycophancy_testing_all_IDs.py`: Performs sycophancy testing across all identity pairs

## Methodology

This research employs a novel methodological approach to detect and measure sycophantic behavior in large language models:

1. **Dataset Generation**: The research uses two types of datasets:
   - **Political Identity Dataset**: Generated using `dataset_generation_political.py`, which creates pairs of opposing political identities (e.g., liberals/conservatives, collectivists/individualists) with corresponding user profiles and questions where these identities would have opposing views.
   - **Moral Foundations Theory (MFT) Dataset**: Generated using `dataset_generation_MFT.py`, which creates datasets based on moral foundation pairs (e.g., care/harm vs. authority/subversion) to test implicit moral sycophancy.

2. **Sycophancy Testing**: The `sycophancy_testing_all_IDs.py` script tests how language models respond to the same questions when presented with different user profiles representing opposing political views or moral foundations. The script:
   - Uses the OpenAI API to interact with GPT-3.5 and GPT-4 models
   - Presents each model with user profiles and political/moral questions
   - Records the model's response probability for agreeing with the profile's expected stance
   - Compares responses across different profiles to measure sycophantic behavior

3. **Data Analysis**: The research uses probabilistic output analysis to measure how models change their responses based on user profiles:
   - Converts log probabilities to percentages to measure agreement levels
   - Compares agreement levels across different user profiles for the same questions
   - Analyzes baseline responses (without user profiles) to establish model bias

## Key Scripts and Their Functions

### Dataset Generation

- **dataset_generation_political.py**: Generates datasets for testing political sycophancy using Google's Vertex AI API with Gemini 1.5 Pro. The script:
  - Uses few-shot learning with examples for different political identity pairs
  - Generates questions on various topics (Technology, Healthcare, Climate Change, etc.)
  - Creates opposing user profiles with biographical details
  - Outputs JSON files with questions and answer options that align with each identity

- **dataset_generation_MFT.py**: Similar to the political dataset generator but creates datasets for testing moral foundation theory pairs to analyze implicit moral sycophancy.

### Sycophancy Testing

- **sycophancy_testing_all_IDs.py**: The core testing script that:
  - Iterates through all identity pairs (political and moral)
  - For each pair, presents models with the same question but different user profiles
  - Uses OpenAI's API to get log probabilities for different response options
  - Measures how models change their responses based on the user profile
  - Stores results in JSON files for further analysis

### Data Processing and Visualization

- **generate_plots.py**: Creates visualizations of the sycophancy testing results:
  - Calculates average agreement levels across topics for each identity pair
  - Converts log probabilities to percentages
  - Creates dot plots comparing agreement levels across different political identities and moral foundations

- **plots.ipynb**: Jupyter notebook containing additional code for generating more complex visualizations and statistical analysis.

### Utility Scripts
- **utils/convert_data_to_csv.py**: Converts the JSON output from testing into CSV format for easier analysis and visualization.
- **utils/count_jsonl_entries.py**: Utility script to count entries in JSONL files.
- **utils/count_json_arrays.py**: Utility script to count entries in JSON array files.

## Data Sets

The `datasets` directory contains data organized by identity pairs:

- Political identity pairs (e.g., liberals_conservatives, socialists_capitalists)
- Moral foundation pairs (e.g., care_harm_authority_subversion)

Each pair directory contains JSON files with questions, user profiles, and answer options tailored to test specific aspects of sycophancy.

## Results and Key Findings

The research found that both GPT-3.5 and GPT-4:

1. Exhibit significant political and moral sycophancy, changing their outputs based on the user's stated affiliations
2. Typically have a fairly left-leaning baseline but change their outputs to align with right-wing ideologies when prompted with right-wing profiles

The visualizations in the `Visualisations` directory provide graphical representations of these findings across different identity pairs and models.

## Running the Code

To replicate this research:

1. For dataset generation:
   - Set up a Google Cloud project and API key for `dataset_generation_political.py` and `dataset_generation_MFT.py`
   - Update the `project_name` variable in these scripts

2. For sycophancy testing:
   - Obtain an OpenAI API key
   - Run `sycophancy_testing_all_IDs.py` (can be configured to use either GPT-3.5 or GPT-4)

3. For visualization:
   - Run `utils/convert_data_to_csv.py` to convert the JSON output from testing into CSV format for easier analysis and visualization.
   - Run `generate_plots.py` to generate dot plots
   - Use `plots.ipynb` for additional visualizations and analysis

## Conclusion

The findings of this study highlight a remarkable level of adaptability in modern LLMs, particularly in how they align with user political and moral views. This research raises important questions about the implications of such sycophantic behavior for deliberative democratic processes and the role of AI in public discourse.
