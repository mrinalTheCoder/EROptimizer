from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import math

load_dotenv()

api_key2 = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key2)
gpt_model = "gpt-3.5-turbo"

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
cc_embeddings = np.load("cc_embeddings.npy")
pmh_embeddings = np.load("pmh_embeddings.npy")

sev_words = ['heart attack', 'seizure', 'stroke']
sev_encodings = model.encode(sev_words)

cc_sev_scores = np.zeros((cc_embeddings.shape[0], len(sev_words)))
pmh_sev_scores = np.zeros((pmh_embeddings.shape[0], len(sev_words)))

for i in range(len(sev_words)):
    for j in range(cc_embeddings.shape[0]):
        cc_sev_scores[j][i] = np.dot(cc_embeddings[j], sev_encodings[i]) / (np.linalg.norm(cc_embeddings[j]) * np.linalg.norm(sev_encodings[i]))

    for j in range(pmh_embeddings.shape[0]):
        pmh_sev_scores[j][i] = np.dot(pmh_embeddings[j], sev_encodings[i]) / (np.linalg.norm(pmh_embeddings[j]) * np.linalg.norm(sev_encodings[i]))

cc_sev_scores = list(np.max(cc_sev_scores, axis=1))
pmh_sev_scores = list(np.mean(pmh_sev_scores, axis=1))

def get_max_cc_score(cc_indices):
    max = 0
    for i in cc_indices:
        if cc_sev_scores[i] > max:
            max = cc_sev_scores[i]
    return max

def get_avg_pmh_score(pmh_indices):
    sum = 0
    for i in pmh_indices:
        sum += pmh_sev_scores[i]
    if (sum == 0):
        return 0
    else: 
        return sum / len(pmh_indices)

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
    
    return output_list

def get_triage(words):
    cc_words = []
    other_words = []

    for word in words:
        if word.startswith('cc_'):
            cc_words.append(word)
        else:
            other_words.append(word)

    cc_indices = [cc_cols.index(word) for word in cc_words]
    pmh_indices = [pmh_cols.index(word) for word in other_words]

    cc_max = get_max_cc_score(cc_indices)
    pmh_avg = get_avg_pmh_score(pmh_indices)

    if(cc_max > pmh_avg):
        triage_index = cc_max
    else:
        triage_index = (cc_max + pmh_avg)/2
    
    if triage_index > 0.5:
        return 1
    elif triage_index > 0.43:
        return 2
    elif triage_index > 0.334:
        return 3
    elif triage_index > 0.2:
        return 4
    else:
        return 5

if __name__ == "__main__":
    print(get_triage(['cc_cardiacarrest']))
