import streamlit as st
import requests

st.title("AI RESUME SCREENER")
st.write("Paste your resume and job description here to check the match")

resume_text=st.text_area("Paste your Resume text here:",height=200)
jd_text=st.text_area("Paste the job description text here",height=200)

if st.button("Check Match"):
    if resume_text and jd_text:
        response=requests.post(
            "http://127.0.0.1:8000/checkmatch",
            json={"resume_text":resume_text,"jd_text":jd_text}
        )
        if response.status_code==200:
            result=response.json()
            st.write(f"**Match Score:** {result['match_percentage']}%")
            st.write(f"**Missing Skills:** {','.join(result['missing_skills'])}")
            st.write("**AI Feedback:**")
            st.write(result['feedback'])
        else:
            st.write("Error:Could not get response")    
    else:
        st.write("Please paste both Resume and Job Description")    