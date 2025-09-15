# app.py 

from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
import streamlit as st
import google.generativeai as genai

# =========================
# Gemini setup
# =========================
GENAI_KEY = os.getenv("GOOGLE_API_KEY")
if GENAI_KEY:
    genai.configure(api_key=GENAI_KEY)
MODEL_ID = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_ID)

# =========================
# Page & Theme
# =========================
st.set_page_config(
    page_title="AI Resume Keyword Matcher",
    page_icon="🧠",
    layout="wide",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "AI Resume Keyword Matcher — powered by Gemini"
    },
)

# Accent color palette (pick one in the sidebar)
PALETTES = {
    "Blueberry": {"accent": "#2563EB", "accent-2": "#1E40AF"},
    "Emerald": {"accent": "#10B981", "accent-2": "#047857"},
    "Purple": {"accent": "#7C3AED", "accent-2": "#5B21B6"},
    "Rose": {"accent": "#F43F5E", "accent-2": "#9F1239"},
    "Amber": {"accent": "#F59E0B", "accent-2": "#B45309"},
}

def inject_css(accent="#2563EB", accent2="#1E40AF"):
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --accent: {accent};
                --accent-2: {accent2};
                --bg-grad-1: rgba(99,102,241,0.06);
                --bg-grad-2: rgba(59,130,246,0.06);
                --card-bg: rgba(255,255,255,0.75);
            }}

            /* App base */
            html, body, [class*="stApp"] {{
                font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans";
                background: radial-gradient(1100px 600px at 10% -10%, var(--bg-grad-1), transparent),
                            radial-gradient(800px 500px at 100% 0%, var(--bg-grad-2), transparent);
            }}

            /* Title (centered, gradient) */
            .app-title {{
                font-family: Poppins, Inter, sans-serif;
                font-weight: 700;
                letter-spacing: 0.2px;
                font-size: 2.4rem;
                margin-bottom: 0.2rem;
                background: linear-gradient(90deg, var(--accent), var(--accent-2));
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                text-align: center;
            }}
            .subtitle {{
                color: #6b7280;
                margin-bottom: 1.2rem;
                text-align: center;
            }}

            /* Section headings: gradient theme */
            h2, h3, h4, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
                font-family: Poppins, Inter, sans-serif;
                font-weight: 600;
                letter-spacing: 0.2px;
                background: linear-gradient(90deg, var(--accent), var(--accent-2));
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent !important;
            }}

            /* Ensure ALL markdown body text (not headings) is black */
            [data-testid="stMarkdownContainer"] :not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) {{
                color: #0f172a !important;
                background: transparent !important;
            }}

            /* Cards */
            .card {{
                background: var(--card-bg);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(100,116,139,0.18);
                border-radius: 16px;
                padding: 18px 18px;
                box-shadow: 0 10px 24px rgba(0,0,0,0.08);
            }}

            /* Buttons */
            .stButton > button {{
                border-radius: 12px;
                padding: 0.6rem 1rem;
                font-weight: 600;
                border: 1px solid transparent;
                background: linear-gradient(90deg, var(--accent), var(--accent-2));
                color: #fff;
            }}
            .stButton > button:hover {{ filter: brightness(0.95); }}

            /* Inputs — force white */
            .stTextArea textarea,
            .stTextInput input {{
                background-color: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #d1d5db !important;
                border-radius: 12px !important;
            }}
            .stTextArea textarea::placeholder,
            .stTextInput input::placeholder {{ color: #6b7280 !important; }}

            /* File uploader — white with themed border + dark text */
            [data-testid="stFileUploaderDropzone"] {{
                background-color: #ffffff !important;
                border: 2px dashed var(--accent) !important;
                border-radius: 12px !important;
                color: #0f172a !important;
                padding: 1rem !important;
                text-align: center !important;
            }}
            [data-testid="stFileUploaderDropzone"] div,
            [data-testid="stFileUploaderDropzone"] * {{
                background-color: transparent !important;
                color: #0f172a !important;
            }}
            [data-testid="stFileUploaderDropzone"] svg {{ fill: var(--accent) !important; }}
            [data-testid="stFileUploaderDropzone"] button {{
                background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.4rem 0.8rem !important;
                font-weight: 600 !important;
            }}

            /* Toast content — white text */
            [data-testid="stNotificationContent"] {{
                color: #ffffff !important;
                font-weight: 600 !important;
            }}

            /* Sidebar — white background + dark text */
            section[data-testid="stSidebar"] {{
                background-color: #ffffff !important;
                color: #0f172a !important;
            }}
            section[data-testid="stSidebar"] * {{
                color: #0f172a !important;
                background-color: transparent !important;
            }}
            /* Sidebar headings get the same gradient theme */
            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] h4 {{
                font-family: Poppins, Inter, sans-serif;
                font-weight: 600;
                letter-spacing: 0.2px;
                background: linear-gradient(90deg, var(--accent), var(--accent-2));
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent !important;
            }}

            /* Footer */
            .footer {{
                margin-top: 1.2rem;
                font-size: 0.86rem;
                color: #6b7280;
                text-align: center;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )



# Sidebar — accent selector + notes
with st.sidebar:
    st.markdown("### 🎨 Theme")
    choice = st.selectbox("Accent color", list(PALETTES.keys()), index=0)
    inject_css(PALETTES[choice]["accent"], PALETTES[choice]["accent-2"])

    st.markdown("---")
    st.markdown("### ℹ️ Tips")
    st.markdown(
        "- Use a focused job description for best results.\n"
        "- Upload the most recent version of your resume.\n"
        "- Try both analysis modes for different perspectives."
    )
    st.markdown("---")
    st.caption("Need Poppler? macOS: `brew install poppler` • Ubuntu: `sudo apt-get install poppler-utils` • Windows: add `C:\\poppler\\bin` to PATH.")

# Header
st.markdown('<div class="app-title">AI Resume Keyword Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze how well your resume aligns with a job description, highlight missing keywords, and get focused feedback.</div>', unsafe_allow_html=True)

# =========================
# Helpers
# =========================
def upload_pdf_to_gemini(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    suffix = ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    file_obj = genai.upload_file(path=temp_path)
    return file_obj

def get_gemini_response(context_text, file_obj, job_description):
    resp = model.generate_content([context_text, file_obj, job_description])
    return getattr(resp, "text", "") or ""

# =========================
# Layout
# =========================
left, right = st.columns([6, 5], gap="large")

with left:
    st.markdown("#### Job Description")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        input_text = st.text_area(
            "Paste the job description here",
            key="job_desc",
            height=220,
            label_visibility="collapsed",
            placeholder="Paste the role responsibilities, requirements, and preferred skills…",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Upload Resume (PDF)")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"], label_visibility="collapsed")
        if uploaded_file is not None:
            st.success(f"Uploaded: **{uploaded_file.name}** • {uploaded_file.size/1024:.0f} KB")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Choose Analysis Mode")
    tabs = st.tabs(["🧭 HR Review", "📈 Percentage Match"])

with right:
    st.markdown("#### Results")
    result_box = st.container()
    with result_box:
        st.markdown('<div class="card results-card">', unsafe_allow_html=True)  #  add results-card
        output_area = st.empty()
        st.markdown("</div>", unsafe_allow_html=True)

# Prompts
input_prompt1 = """
You are an experienced HR professional with strong technical hiring experience
(Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Data Analysis,
Computer Science, Software Engineering). Review the provided resume against the job description.
Assess alignment to the role, and clearly list strengths and weaknesses relative to the requirements.
Provide concise, structured feedback with bullet points and short paragraphs that are skimmable.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) expert for roles such as
Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Data Analysis,
Computer Science, or Software Engineering. Evaluate the resume against the job description.
First output an overall percentage match (0–100%). Then list missing/weak keywords.
Finally provide concise, actionable final thoughts for improvement (3–5 bullets).
"""

# Runner
def run_evaluation(prompt_text):
    if not GENAI_KEY:
        st.error("Missing `GOOGLE_API_KEY`. Add it to your environment and restart.")
        return
    if not input_text or input_text.strip() == "":
        st.warning("Please paste the job description.")
        return
    if uploaded_file is None:
        st.warning("Please upload the resume (PDF).")
        return
    with st.spinner("Analyzing…"):
        try:
            file_obj = upload_pdf_to_gemini(uploaded_file)
            response_text = get_gemini_response(prompt_text, file_obj, input_text)
            if response_text.strip():
                output_area.markdown(response_text)
                st.toast("Done", icon="✅")
            else:
                output_area.info("No content returned. Try again or adjust your inputs.")
        except Exception as e:
            output_area.error(f"Error: {e}")

# Buttons inside tabs
with tabs[0]:
    st.caption("Human-style review: strengths, weaknesses, and alignment to requirements.")
    if st.button("Run HR Review", use_container_width=True):
        run_evaluation(input_prompt1)

with tabs[1]:
    st.caption("ATS-style scoring: % match + missing keywords + concise action items.")
    if st.button("Run Percentage Match", use_container_width=True):
        run_evaluation(input_prompt3)


