# AI-Powered Resume Keyword Matcher

The AI-Powered Resume Keyword Matcher is a simple tool that helps job seekers check how well their resume matches a job description. It uses OpenAI’s API along with keyword matching and similarity techniques to highlight missing keywords and provide a match score. The app is built with Streamlit, making it easy to use in your browser.

## Features
- Upload resumes in PDF, DOCX, or TXT format
- Automatically extracts text from resumes
- Compare your resume with a job description
- Shows a similarity score and missing keywords
- Easy-to-use interface in your browser

## Installation and Setup
1. Clone or download this project from GitHub.  
   ```bash
   git clone https://github.com/<msaad26>/AI-Powered-Resume-Keyword-Matcher.git
   cd AI-Powered-Resume-Keyword-Matcher

## Create a Virtual Environment and Activate It

### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### On Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

## Poppler Installation (Required for PDF Support)

### On macOS/Linux:
```bash
brew install poppler
```
### On Windows
1. Download Poppler for Windows (search for Poppler Windows Release on GitHub).
2. Extract the folder, for example to C:\poppler.
3. Add C:\poppler\bin to your system PATH.

## Running Application
```bash
streamlit run app.py
```

## Dependencies
This project uses the following Python packages:  

- `streamlit` – for the app  
- `openai` – to connect with OpenAI API  
- `scikit-learn` – for similarity calculations  
- `pdf2image` – to process PDFs  
- `docx2txt` – to process DOCX files  
- `PyPDF2` – to read text from PDFs  








