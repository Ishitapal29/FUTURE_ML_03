import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

st.set_page_config(page_title="AI Resume Screening")
st.title("AI-Based Resume Screening and Ranking System")

job_description = st.text_area("Enter the job description")

uploaded_resumes = st.file_uploader(
    "Upload resumes (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

def extract_text(file):
    if file.name.lower().endswith(".txt"):
        return file.getvalue().decode("utf-8", errors="ignore")

    reader = PdfReader(file)
    return " ".join(
        page.extract_text() or "" for page in reader.pages
    )

def find_skills(text):
    skills = [
        "python", "sql", "machine learning", "data analysis",
        "pandas", "excel", "communication", "statistics",
        "java", "c++", "deep learning", "nlp", "git"
    ]
    text = text.lower()
    return [skill for skill in skills if skill in text]

if st.button("Screen Resumes"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_resumes:
        st.warning("Please upload at least one resume.")
    else:
        resume_texts = []
        candidate_names = []

        for file in uploaded_resumes:
            try:
                text = extract_text(file)
                if text.strip():
                    resume_texts.append(text)
                    candidate_names.append(file.name)
                else:
                    st.warning(f"No readable text found in {file.name}.")
            except Exception as error:
                st.warning(f"Could not read {file.name}: {error}")

        if resume_texts:
            documents = [job_description] + resume_texts
            vectorizer = TfidfVectorizer(stop_words="english")
            matrix = vectorizer.fit_transform(documents)
            scores = cosine_similarity(
                matrix[0:1], matrix[1:]
            ).flatten()

            job_skills = set(find_skills(job_description))
            results = []

            for name, text, score in zip(
                candidate_names, resume_texts, scores
            ):
                resume_skills = set(find_skills(text))
                matched = sorted(job_skills & resume_skills)
                missing = sorted(job_skills - resume_skills)

                coverage = (
                    len(matched) / len(job_skills)
                    if job_skills else 0
                )

                final_score = (
                    0.6 * float(score) + 0.4 * coverage
                ) * 100

                results.append({
                    "Candidate": name,
                    "Score (%)": round(final_score, 2),
                    "Matched skills": ", ".join(matched) or "None detected",
                    "Missing skills": ", ".join(missing) or "None detected"
                })

            results.sort(
                key=lambda item: item["Score (%)"],
                reverse=True
            )

            st.subheader("Candidate Ranking")
            st.dataframe(results, use_container_width=True)

            st.download_button(
                "Download results as CSV",
                data=__import__("pandas").DataFrame(
                    results
                ).to_csv(index=False).encode("utf-8"),
                file_name="resume_ranking.csv",
                mime="text/csv"
            )