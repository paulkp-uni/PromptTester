import streamlit as st
import json
import random
import pandas as pd
import matplotlib.pyplot as plt

# Dummy functions to simulate LLM responses
def dummy_llm_1(system_prompt, query):
    return f"Response to {query} with prompt {system_prompt}"

def dummy_llm_2(query, response, criterion):
    return random.randint(0, 10)

# Function to load JSON data
def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save JSON data
def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# UI for the app
st.title("LLM System Prompt Testing")

# Input, display, and edit system prompts
st.header("System Prompts")
stored_system_prompts = load_json("system_prompts.json")
system_prompts = st.text_area("Enter system prompts (one per line)", "\n".join(stored_system_prompts), height=200)
system_prompts_list = system_prompts.split('\n')

if st.button("Save System Prompts"):
    save_json(system_prompts_list, "system_prompts.json")

# Input, display, and edit queries and test criteria
st.header("Queries and Test Criteria")
stored_queries_criteria = load_json("queries_criteria.json")
queries = st.text_area("Enter queries (one per line)", "\n".join(stored_queries_criteria.get("queries", [])), height=100)
criteria = st.text_area("Enter corresponding test criteria (one per line)", "\n".join(stored_queries_criteria.get("criteria", [])), height=100)
queries_list = queries.split('\n')
criteria_list = criteria.split('\n')

if st.button("Save Queries and Criteria"):
    data = {"queries": queries_list, "criteria": criteria_list}
    save_json(data, "queries_criteria.json")

# Test loop
st.header("Run Test Loop")
if st.button("Run Test"):
    results = {}
    for query in queries_list:
        for system_prompt in system_prompts_list:
            response = dummy_llm_1(system_prompt, query)
            criterion = criteria_list[queries_list.index(query)]
            score = dummy_llm_2(query, response, criterion)
            if system_prompt not in results:
                results[system_prompt] = []
            results[system_prompt].append(score)
    save_json(results, "results.json")

# Display results
st.header("Results")
results = load_json("results.json")
st.write(results)

# Calculate and display averages
if results:
    averages = {prompt: sum(scores) / len(scores) for prompt, scores in results.items()}
    df = pd.DataFrame(list(averages.items()), columns=['System Prompt', 'Average Score'])
    st.write(df)

    # Plot averages
    st.subheader("Average Scores")
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(df)), df['Average Score'])
    plt.xlabel('Prompt Version Index')
    plt.ylabel('Average Score')
    plt.title('Average Score vs System Prompt Versions')
    plt.xticks(range(len(df)), range(len(df)))
    plt.tight_layout()
    st.pyplot(plt)
