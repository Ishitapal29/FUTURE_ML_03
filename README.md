# FUTURE_ML_03
An AI-based resume screening system that uses NLP, TF-IDF, and cosine similarity to rank resumes against a job description and identify matching skills.
AI-Based Resume Screening and Ranking System

Project Overview:- 
This project uses Natural Language Processing (NLP) techniques to compare resumes with a job description and rank candidates based on how closely their skills and experience match the requirements.

Features
- Upload multiple resumes in PDF or TXT format.
- Enter a job description.
- Extract text from resumes.
- Calculate resume similarity using TF-IDF and cosine similarity.
- Identify matched and missing skills.
- Rank candidates by matching score.
- Download ranking results as a CSV file.

Technologies Used
- Python
- Streamlit
- PyPDF
- Scikit-learn
- Pandas

How to Run
1. Install Python.
2. Install the required libraries:
   "py -m pip install -r requirements.txt"
3. Run the application:
   "py -m streamlit run app1.py"
4. Open the local URL displayed in the terminal.

This is an educational project. The ranking score is an automated estimate of text and skill similarity, not a definitive measure of a candidate's suitability. Candidate rankings should be reviewed by a human.
