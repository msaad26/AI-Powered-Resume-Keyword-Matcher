from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import tempfile
import google.generativeai as genai

# -------------------------
# Gemini setup
# -------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-1.5-flash"   # or "gemini-1.5-pro"
model = genai.GenerativeModel(MODEL_ID)

# -------------------------
# Helpers
# -------------------------
def upload_pdf_to_gemini(uploaded_file):
    """
    Save the Streamlit UploadedFile to a temp file and upload it to Gemini.
    Returns a genai File object you can pass to generate_content.
    """
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    # Persist to a temp path so the SDK can upload by path
    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    # Upload to Gemini Files API
    file_obj = genai.upload_file(path=temp_path)
    return file_obj

def get_gemini_response(context_text, file_obj, job_description):
    """
    context_text: your role/prompt (HR/ATS instructions)
    file_obj: the uploaded PDF 'File' returned by upload_file
    job_description: string from the textarea
    """
    resp = model.generate_content([context_text, file_obj, job_description])
    return resp.text

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="AI Resume Keyword Matcher")
st.header("AI Resume Keyword Matcher")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully.")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR professional with strong technical hiring experience
(Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Data Analysis,
Computer Science, Software Engineering). Review the provided resume against the job description.
Assess alignment to the role, and clearly list strengths and weaknesses relative to the requirements.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) expert for roles such as
Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Data Analysis,
Computer Science, or Software Engineering. Evaluate the resume against the job description.
First output an overall percentage match (0–100%). Then list missing/weak keywords.
Finally provide concise, actionable final thoughts for improvement.
"""

def run_evaluation(prompt_text):
    if uploaded_file is None:
        st.warning("Please upload the resume.")
        return
    try:
        file_obj = upload_pdf_to_gemini(uploaded_file)
        response_text = get_gemini_response(prompt_text, file_obj, input_text)
        st.subheader("The Response")
        st.write(response_text if response_text else "No content returned.")
    except Exception as e:
        st.error(f"Error: {e}")

if submit1:
    run_evaluation(input_prompt1)
elif submit3:
    run_evaluation(input_prompt3)
