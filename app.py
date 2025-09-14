from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
from PIL imoport Image
import pdf2image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-prp-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## COnvert pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page=images[0]
        
        
        #Convert to bytes
        img_byte_arr = io. BytesIO)
        first_page. save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr-getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.64encode(img_byte_arr). decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundEroor("No File Uploaded")
    
    
## Streamlit App

st.set_page_confiq(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
submit1 = st.button("Tell Me About The Resume")

submit2 = st.button("How Can I Improve my Skills")

submit3 = st.button("Percentage Match")

input_prompt1 = """


You are an experienced HR With Tech Experience in the filed of Dtaa Science, Full stack
Web development, Big Data Engineering, DEVOPS,Data Analyst, computer science, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether