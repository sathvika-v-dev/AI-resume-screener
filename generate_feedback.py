import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import sqlite3
load_dotenv()
groq_client=Groq(api_key=os.getenv("GROQ_API_KEY"))
model=HuggingFaceEmbeddings(model_name="sentence-transformer/all-MiniLM-L6-v2")

resume_text="""
Experienced Python developer with skills in machine learning,NLP,FastAPI,and SQL.Worked on building REST APIs and data pipeline using pandas and scikit-learn
"""
jd_text="""
Looking for a Python Developer with experience in machine learning,deep learning,NLP,FastAPI,Docker,and kubernetes.Must have strong SQL skills and experience with cloud platforms like AWS
"""
skills_list=[
    "python","machine learning","deep learning","nlp","fastAPI","sql","docker","kubernetes","aws","pandas","scikit-learn","flask","django","react","javascript","java","c++","tensorflow","pytorch","restapi","git","linux"
]
resume_embedding=model.encode([resume_text])
jd_embedding=model.encode([jd_text])
similarity_score=cosine_similarity(resume_embedding,jd_embedding)[0][0]
match_percentage=round(similarity_score*100,2)
resume_lower=resume_text.lower()
jd_lower=jd_text.lower()
jd_skills=[skill for skill in skills_list if skill in jd_lower]
resume_skills=[skill for skill in jd_skills if skill not in resume_lower]
missing_skills=[skill for skill in jd_skills if skill not in resume_skills]
prompt=f"""you are a resume screening assistant.Based on the following data,give short,accountable feedback to the candidate.
Match Score:{match_percentage}
skills required for job:{','.join(jd_skills)}
skills found in resume:{','.join(resume_skills)}
Missing skills:{','.join(missing_skills)}
Give a 3-4 sentence summary explaining the match quality and what the candidate should improve.
"""
response=groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role":"system","content":"you are a helpful resume screening assistant"},
        {"role":"user","content":prompt}
    ]
)
feedback=response.choices[0].message.content
print(f"match score:{match_percentage}%")
print(f"missing skills:{missing_skills}")
print("---")
print("AI Feedback:")
print(feedback)


conn=sqlite3.connect("resume_checks.db")
cursor=conn.cursor() 
cursor.execute(
    "INSERT INTO resume_checks(match_percentage,missing_skills,feedback)VALUES(?,?,?)",
    (match_percentage,",".join(missing_skills),feedback)
)
conn.commit()
conn.close()