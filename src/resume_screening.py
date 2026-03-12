from flask import Flask, render_template, request
import os
import pandas as pd
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_resumes(folder):
    names = []
    texts = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            text = extract_text(path)

            names.append(file)
            texts.append(text)

    return names, texts


def calculate_scores(job_desc, resumes):

    documents = [job_desc] + resumes

    vectorizer = CountVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    return similarity


@app.route("/", methods=["GET", "POST"])
def index():

    results = None

    if request.method == "POST":

        job_description = request.form["job_description"]

        files = request.files.getlist("resumes")

        for file in files:
            if file.filename.endswith(".pdf"):
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))

        names, resumes = extract_resumes(UPLOAD_FOLDER)

        scores = calculate_scores(job_description, resumes)

        data = pd.DataFrame({
            "Applicant": names,
            "Score": scores
        })

        results = data.sort_values(by="Score", ascending=False)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
