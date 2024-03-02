from PyPDF2 import PdfReader
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv() ##load all our enviroment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text)
    return text

#propmt template
input_propmt="""
Hey Act like a skilledor very experience ATS(application tracking system) with deep
understanding of each field, software egineering, data science, data analyst and Big data enginner
Your task to evaulate the resume based on given description. You must consider the Job market is
very competitive and you should best assistance for improving the resumes. Percentage matching
based on JD and missing Keywords with high accuracy 
resume:{text}
description:{jd}

I want the response in single string having a structure
{{"JD Match":"%","Missing_Keywords:[]", "Profile summary":""}}


"""


#streamlit
st.title("Smart ATS System")
st.text("Improve Your Resume ATS")
jd=st.text_area("paste the Job Description(JD)")
uploaded_file=st.file_uploader("Upload your resume",type='pdf',help="Please upload the Pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file  is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_propmt)
        st.subheader(response)
      