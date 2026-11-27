import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

skills_list = [
    "python", "machine learning", "deep learning", "nlp", "fastapi", "sql",
    "docker", "kubernetes", "aws", "pandas", "scikit-learn", "flask",
    "django", "react", "javascript", "java", "c++", "tensorflow",
    "pytorch", "restapi", "git", "linux",
]


@st.cache_resource
def load_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


st.title("AI RESUME SCREENER")
st.write("Paste your resume and job description here to check the match")

resume_text = st.text_area("Paste your Resume text here:", height=200)
jd_text = st.text_area("Paste the job description text here:", height=200)

if st.button("Check Match"):
    if resume_text and jd_text:
        with st.spinner("Analyzing..."):
            model = load_model()
            resume_embedding = [model.embed_query(resume_text)]
            jd_embedding = [model.embed_query(jd_text)]
            similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
            match_percentage = round(similarity_score * 100, 2)

            resume_lower = resume_text.lower()
            jd_lower = jd_text.lower()
            jd_skills = [s for s in skills_list if s in jd_lower]
            resume_skills = [s for s in skills_list if s in resume_lower]
            missing_skills = [s for s in jd_skills if s not in resume_skills]

            prompt = f"""You are a resume screening assistant. Based on the following data, give short, actionable feedback to the candidate.

Match Score: {match_percentage}%
Skills required for the job: {', '.join(jd_skills)}
Skills found in resume: {', '.join(resume_skills)}
Missing skills: {', '.join(missing_skills)}

Give a 3-4 sentence summary explaining the match quality and what the candidate should improve."""

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are a helpful resume screening assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            feedback = response.choices[0].message.content

        st.write(f"**Match Score:** {match_percentage}%")
        st.write(f"**Missing Skills:** {', '.join(missing_skills)}")
        st.write("**AI Feedback:**")
        st.write(feedback)
    else:
        st.write("Please paste both Resume and Job Description")