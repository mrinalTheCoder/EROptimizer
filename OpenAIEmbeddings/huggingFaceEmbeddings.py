import numpy as np
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

gender = "Male"
age = 19

json_file_path = "/Users/kaustubhbhal/Hacklytics/EROptimizer/OpenAIEmbeddings/output.json"

# Read JSON data from the file
with open(json_file_path, "r") as file:
    data = json.load(file)

# Create a new dictionary with lowercase keys and values
lowercase_data = {}
for key, value in data.items():
    lowercase_data[key.lower()] = value.lower() if isinstance(value, str) else value

# Write the modified JSON data back to the file
with open(json_file_path, "w") as file:
    json.dump(lowercase_data, file, indent=4)

with open(json_file_path, "r") as file:
    json_data = json.load(file) 

complaints_str = json_data["complaints"]
past_medical_history_str = json_data["past medical history"]

current_complaints = [complaint.strip().lower() for complaint in complaints_str.split(",")]
past_medical_history = [history.strip().lower() for history in past_medical_history_str.split(",")]

#print("Current Complaints:", current_complaints)
#print("Past Medical History:", past_medical_history)

#current_complaints = ["broken left arm"]
#past_medical_history = ["Asthma", "Obesity"]

with open("training/cc_cols.txt", "r") as f:
    cc_cols = f.readlines()
cc_cols = list(map(lambda x:x[:-1], cc_cols))

with open("training/pmh_cols.txt", "r") as f:
    pmh_cols = f.readlines()
pmh_cols = list(map(lambda x:x[:-1], pmh_cols))
# outputList = []

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
cc_embeddings = np.load("OpenAIEmbeddings/cc_embeddings.npy")
pmh_embeddings = np.load("OpenAIEmbeddings/pmh_embeddings.npy")
def col_embeddings_to_file(sentences, path):
    embeddings = model.encode(sentences)
    np.save(path, embeddings)

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

    # similarity = 0
    # for w1 in words1:
    #     for w2 in words2:
    #         sentences = [w1, w2]
    #         model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    #         embeddings = model.encode(sentences)
    #         sim_score = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    #         if(sim_score > 0.3):
    #             outputList.append(1)
    #         else:
    #             outputList.append(0)


# col_embeddings_to_file(cc_cols, "cc_embeddings.npy")
# col_embeddings_to_file(pmh_cols, "pmh_embeddings.npy")
