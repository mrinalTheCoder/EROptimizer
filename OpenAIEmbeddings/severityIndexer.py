import numpy as np

from huggingFaceEmbeddings import compute_similarity, current_complaints, past_medical_history

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open("training/cc_cols.txt", "r") as f:
    cc_cols = f.readlines()
cc_cols = list(map(lambda x:x[:-1], cc_cols))

with open("training/pmh_cols.txt", "r") as f:
    pmh_cols = f.readlines()
pmh_cols = list(map(lambda x:x[:-1], pmh_cols))

cc_embeddings = np.load("OpenAIEmbeddings/cc_embeddings.npy")
pmh_embeddings = np.load("OpenAIEmbeddings/pmh_embeddings.npy")

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

_, __, out = compute_similarity(current_complaints, past_medical_history)

cc_words = ["cc_breathingdifficulty", "cc_breathingproblem"]
other_words = ["asthma"]

# for word in out:
#     if word.startswith('cc_'):
#         cc_words.append(word)
#     else:
#         other_words.append(word)
    
print(cc_words)
print(other_words)

cc_indices = [cc_cols.index(word) for word in cc_words]
pmh_indices = [pmh_cols.index(word) for word in other_words]

# temp_pmh = [(i, pmh_sev_scores[i]) for i in range(len(pmh_sev_scores))]
# max_score_pmh = max(temp_pmh, key=lambda x:x[1])
# min_score_pmh = min(temp_pmh, key=lambda x:x[1])

# temp_cc = [(i, cc_sev_scores[i]) for i in range(len(cc_sev_scores))]
# max_score_cc = max(temp_cc, key=lambda x:x[1])
# min_score_cc = min(temp_cc, key=lambda x:x[1])

#print(max_score)
# print(pmh_cols[max_score_pmh[0]])
# print(cc_cols[max_score_cc[0]])

# print(pmh_cols[min_score_pmh[0]])
# print(cc_cols[min_score_cc[0]])

cc_max = get_max_cc_score(cc_indices)
pmh_avg = get_avg_pmh_score(pmh_indices)

print(cc_max)


if(cc_max > pmh_avg):
    triage_index = cc_max
else:
    triage_index = (cc_max + pmh_avg)/2

print(triage_index)

if triage_index > 0.5:
    print("Level 1")
elif triage_index > 0.43:
    print("Level 2")
elif triage_index > 0.334:
    print("Level 3")
elif triage_index > 0.2:
    print("Level 4")
else:
    print("Level 5")