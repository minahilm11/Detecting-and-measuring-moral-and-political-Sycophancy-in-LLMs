# Moral and Political Sycophancy in Large Language Models

This repository contains code and data for my Master's thesis project investigating moral and political sycophancy in large language models (LLMs). The thesis analyzes the implications of LLMs exhibiting sycophantic behaviour, where they align their responses to match users' moral and political views, for deliberative democracy. 

## Repository Structure

- `csv_data/`: Directory containing CSV data files used in the analysis 
- `data_gpt_3.5/`: GPT-3.5 model data and outputs
- `data_gpt_4/`: GPT-4 model data and outputs  
- `dataset_gen_prompts/`: Prompts used for generating the sycophancy testing datasets
- `datasets/`: Generated datasets for sycophancy testing
- `few_shot_examples/`: Few-shot learning examples used to prime the models
- `convert_data_to_csv.py`: Script to convert data to CSV format
- `dataset_generation_MFT.py`: Generates moral foundations theory dataset for implicit sycophancy testing
- `dataset_generation_political.py`: Generates political identities dataset for explicit sycophancy testing
- `plots.ipynb`: Jupyter notebook with code for generating plots and visualizations
- `prompt_MFT.txt`: Text file with prompts for moral foundations testing
- `prompt_political.txt`: Text file with prompts for political identity sycophancy testing  
- `README.MD`: This readme file
- `sycophancy_barplots.py`: Generates bar plot visualizations of sycophancy testing results
- `sycophancy_testing_all_IDs.py`: Performs sycophancy testing across all identity pairs

## Data 
The datasets were generated using gemini-1.0-pro in  `dataset_generation_political.py` and `dataset_generation_MFT.py`.
The `datasets` directory contains the generated datasets used for sycophancy testing of the GPT-3.5 and GPT-4 models. The `csv_data` folder has the data in CSV format. Model outputs are stored in the `data_gpt_3.5` and `data_gpt_4` folders.

## Analysis
The main analysis code is in the `sycophancy_testing_all_IDs.py` script which runs the sycophancy tests. Visualizations are generated using `sycophancy_barplots.py` and `plots.ipynb`. 

Refer to the thesis document in the `datasets` folder for full details on the methodology, results and discussion. The abstract summarizes:

> This thesis introduces a novel methodological approach by using machine learning techniques, including few-shot learning, prompt engineering, and probabilistic output analysis, to investigate sycophancy within the fine-tuned models, GPT-3.5 and GPT-4. The results indicate that these models exhibit political and moral sycophancy, meaning that they change their outputs based on the user's moral or political affiliations. Furthermore, the models exhibit a greater propensity to deviate from their baseline responses and align their answers with the political and moral beliefs of right-wing ideologies. The findings of this study highlight a remarkable level of deception among these models and a deep understanding of user preferences.

Please see the full thesis for more details on the background, methodology, results and conclusions of this research project exploring the implications of sycophantic behavior in language models for deliberative democratic processes.
