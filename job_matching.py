import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec
from nlp_model import extract_skills_from_resume

# Load dataset
df = pd.read_csv("jobs.csv")
df["skills"] = df["required_skills"].apply(lambda x: x.lower().split(", ") if isinstance(x, str) else [])

# Load models
word2vec = pickle.load(open("word2vec.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

scaler = StandardScaler()

# Convert skills to vectors
def get_vector(words):
    vectors = [word2vec.wv[word] for word in words if word in word2vec.wv]
    return sum(vectors) / len(vectors) if vectors else None

df["skill_vectors"] = df["skills"].apply(get_vector)
df = df.dropna(subset=["skill_vectors"])

# Train scaler
X = list(df["skill_vectors"])
X_scaled = scaler.fit_transform(X)

def process_resume(filepath):
    extracted_skills = extract_skills_from_resume(filepath)
    skill_vector = get_vector(extracted_skills)

    if skill_vector is None:
        return {"error": "No relevant skills found in resume"}

    predicted_salary = model.predict(scaler.transform([skill_vector]))[0]

    df["similarity"] = df["skill_vectors"].apply(lambda x: np.dot(skill_vector, x) / (np.linalg.norm(skill_vector) * np.linalg.norm(x)))
    
    matched_jobs = df.sort_values(by="similarity", ascending=False).head(7)[
        ["job_role", "companyname", "location", "salary", "applylink"]
    ].to_dict(orient="records")

    return {"predicted_salary": predicted_salary, "matched_jobs": matched_jobs}
