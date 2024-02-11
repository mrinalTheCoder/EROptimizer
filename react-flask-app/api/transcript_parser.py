from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

api_key2 = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key2)
gpt_model = "gpt-3.5-turbo"

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
cc_embeddings = np.load("cc_embeddings.npy")
pmh_embeddings = np.load("pmh_embeddings.npy")

with open("cc_cols.txt", "r") as f:
    cc_cols = f.readlines()
cc_cols = list(map(lambda x:x[:-1], cc_cols))

with open("pmh_cols.txt", "r") as f:
    pmh_cols = f.readlines()
pmh_cols = list(map(lambda x:x[:-1], pmh_cols))

def parse_content(content_string):
    info = {}
    lines = content_string.split("\n")
    for line in lines:
        key, value = line.split(": ")
        info[key.strip().lower()] = value.strip().lower()
    return info

def gpt_response(query):
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": "Given the following speech to text transcription, please provide age, gender, complaints, and past medical history"},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    print("received gpt response")

    response_json = json.loads(response.model_dump_json())
    content_string = response_json['choices'][0]['message']['content']

    return parse_content(content_string)

def compute_similarity(user_cc, user_pmh):
    output_list = []
    user_cc_embeddings = model.encode(user_cc)
    user_pmh_embeddings = model.encode(user_pmh)
    output_ccs = np.zeros(len(cc_embeddings))
    output_pmhs = np.zeros(len(pmh_embeddings))
    for i in range(len(cc_embeddings)):
        for j in range(len(user_cc_embeddings)):
            sim_score = np.dot(user_cc_embeddings[j], cc_embeddings[i]) / (np.linalg.norm(user_cc_embeddings[j]) * np.linalg.norm(cc_embeddings[i]))
            if(sim_score > 0.5):
                output_ccs[i] = 1
                output_list.append(cc_cols[i])
    
    for i in range(len(pmh_embeddings)):
        for j in range(len(user_pmh_embeddings)):
            sim_score = np.dot(user_pmh_embeddings[j], pmh_embeddings[i]) / (np.linalg.norm(user_pmh_embeddings[j]) * np.linalg.norm(pmh_embeddings[i]))
            if(sim_score > 0.5):
                output_pmhs[i] = 1
                output_list.append(pmh_cols[i])
    
    return output_ccs, output_pmhs, output_list
