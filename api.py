from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import sqlite3

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

skills_list = [
    "python", "machine learning", "deep learning", "nlp", "fastapi",
    "sql", "docker", "kubernetes", "aws", "pandas", "scikit-learn",
    "flask", "django", "react", "javascript", "java", "c++",
    "tensorflow", "pytorch", "rest api", "git", "linux"
]

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

@app.get("/")
def home():
    return {"message": "Resume Screener API is running"}

@app.post("/checkmatch")
def check_match(request: MatchRequest):
    resume_text = request.resume_text
    jd_text = request.jd_text

    resume_embedding = [model.embed_query(resume_text)]
    jd_embedding = [model.embed_query(jd_text)]
    similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    match_percentage = round(similarity_score * 100, 2)

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    jd_skills = [skill for skill in skills_list if skill in jd_lower]
    resume_skills = [skill for skill in skills_list if skill in resume_lower]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    prompt = f"""You are a resume screening assistant. Based on the following data, give short, actionable feedback to the candidate.

Match Score: {match_percentage}%
Skills required for the job: {','.join(jd_skills)}
Skills found in resume: {','.join(resume_skills)}
Missing skills: {','.join(missing_skills)}

Give a 3-4 sentence summary explaining the match quality and what the candidate should improve."""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful resume screening assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    feedback = response.choices[0].message.content

    conn = sqlite3.connect("resume_checks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO resume_checks (match_percentage, missing_skills, feedback) VALUES (?, ?, ?)",
        (match_percentage, ','.join(missing_skills), feedback)
    )
    conn.commit()
    conn.close()

    return {
        "match_percentage": match_percentage,
        "missing_skills": missing_skills,
        "feedback": feedback
    }