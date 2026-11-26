resume_text="""
Experienced python developer with skills in machinelearning,NLP,Fastapi,and SQL.Worked on building REST APIs and data pipelines using pandas and scikit-learn."""

jd_text="""
Looking for a python developer with experience in machine learning,deeplearning,NLP,FastAPI,Docker,and Kuberntes.Must have strong SQL Skills and experience with cloud platforms like AWS
"""
#common tech skills
skills_list=[
    "python","machine learning","deep learning","nlp","fastAPI","sql","docker","kubernetes","aws","pandas","scikit-learn","flask","django","react","javascript","java","c++","tensorflow","pytorch","restapi","git","linux"
]
resume_lower=resume_text.lower()
jd_lower=jd_text.lower()

jd_skills=[skill for skill in skills_list if skill in jd_lower]

resume_skills=[skill for skill in skills_list if skill in resume_lower]

missing_skills=[skill for skill in jd_skills if skill not in resume_lower]

print("skills required in JD:",jd_skills)
print("skills found in Resume:",resume_skills)
print("Missing skills in Resume:",missing_skills)