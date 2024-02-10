
from gensim.models import KeyedVectors

# Load pre-trained GloVe embeddings
glove_model = KeyedVectors.load_word2vec_format('/Users/kaustubhbhal/Downloads/glove.6B.100d.txt')

# Given parameters
gender = "Male"
age = 25
current_complaints = ["headache", "broken arm"]
past_medical_history = ["Migraines", "high blood pressure"]

# List of complaints and medical history
complaints = [
    "arm"
    # Add more complaints as needed
]

medical_history = [
    "migraine",
    "high blood pressure"
    # Add more medical history items as needed
]

# Function to get embedding for a word if it exists in the vocabulary
def get_word_embedding(word):
    try:
        return glove_model[word.lower()]  # Convert word to lowercase
    except KeyError:
        return None  # Return None if word is not in vocabulary

# Function to compute similarity between two lists of words
def compute_similarity(words1, words2):
    similarity = 0
    for w1 in words1:
        for w2 in words2:
            emb1 = get_word_embedding(w1)
            emb2 = get_word_embedding(w2)
            if emb1 is not None and emb2 is not None:
                similarity = max(similarity, glove_model.similarity(w1, w2))
    return similarity

# Compute similarity between given parameters and complaints/medical history
complaint_similarity = compute_similarity(current_complaints, complaints)
medical_history_similarity = compute_similarity(past_medical_history, medical_history)

print("Complaint Similarity:", complaint_similarity)
print("Medical History Similarity:", medical_history_similarity)

