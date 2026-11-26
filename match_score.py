from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

#embedding model loading
model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


#sample resume and JD text for testing
resume_text="""
Experienced python developer with skills in machinelearning,NLP,Fastapi,and SQL.Worked on building REST APIs and data pipelines using pandas and scikit-learn.
"""
jd_text="""
Looking for a python developer with experience in machine learning,deeplearning,NLP,FastAPI,Docker,and Kubernetes.Must have strong SQL Skills and experience with cloud platforms like AWS
"""
#converting into embeddings
resume_embedding=[model.embed_query(resume_text)]
jd_embedding=[model.embed_query(jd_text)]
#cosine similarity
similarity_score=cosine_similarity(resume_embedding,jd_embedding)[0][0]
#score as percentage
match_percentage=round(similarity_score*100,2)

print(f"Match Score:{match_percentage}%")
