```python
import os
import pandas as pd
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Folder containing resumes
RESUME_FOLDER = "resumes"

# Example job description
job_description = """
Looking for a software developer with experience in Python, SQL,
data analysis, machine learning, and problem solving.
"""

def extract_resumes(folder):
    resume_names = []
    resume_texts = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            text = extract_text(path)

            resume_names.append(file)
            resume_texts.append(text)

    return resume_names, resume_texts


def calculate_scores(job_desc, resumes):

    documents = [job_desc] + resumes

    vectorizer = CountVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    return similarity


def rank_applicants():

    names, resumes = extract_resumes(RESUME_FOLDER)

    scores = calculate_scores(job_description, resumes)

    data = pd.DataFrame({
        "Applicant": names,
        "Score": scores
    })

    ranked = data.sort_values(by="Score", ascending=False)

    print("\n=== Ranked Applicants ===\n")
    print(ranked)


if __name__ == "__main__":
    rank_applicants()
