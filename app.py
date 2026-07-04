import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI CV Assistant",
    page_icon="📄",
    layout="centered"
)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    document = Document(file)
    return "\n".join([paragraph.text for paragraph in document.paragraphs])

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    return ""

def analyze_cv(cv_text, job_description):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Error: Gemini API key not found. Please add it to your .env file."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI career assistant helping a student improve their internship application.

Analyze the CV against the job description.

Return the answer in this exact structure:

## Overall Match Score
Give a percentage and short explanation.

## Strong Matches
List the candidate's strongest matching skills and experiences.

## Missing or Weak Keywords
List important keywords from the job description that are missing or weak in the CV.

## CV Improvement Suggestions
Give specific suggestions for improving the CV.

## Tailored CV Bullet Points
Rewrite 4-6 bullet points that the candidate could use in their CV.

## Cover Letter Draft
Write a short cover letter tailored to the role.

## Interview Preparation Questions
Give 5 likely interview questions.

CV:
{cv_text}

Job Description:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

st.title("AI-Powered CV and Cover Letter Assistant")

st.write(
    "Upload your CV and paste a job description to receive AI-supported suggestions."
)

uploaded_cv = st.file_uploader(
    "Upload your CV",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste the job description here",
    height=250
)

if st.button("Analyze CV"):
    if uploaded_cv is None:
        st.warning("Please upload your CV.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Extracting CV text...")
        progress_bar.progress(25)

        cv_text = extract_text(uploaded_cv)

        if not cv_text.strip():
            st.error("Could not extract text from the CV. Please try another file.")
        else:
            status_text.text("Sending CV and job description to Gemini...")
            progress_bar.progress(60)

            result = analyze_cv(cv_text, job_description)

            status_text.text("Generating final analysis...")
            progress_bar.progress(100)

            st.success("Analysis completed successfully.")

            tab1, tab2, tab3 = st.tabs([
                "AI Analysis",
                "Export",
                "Project Notes"
            ])

            with tab1:
                st.markdown(result)

            with tab2:
                st.download_button(
                    label="Download Analysis as TXT",
                    data=result,
                    file_name="cv_analysis.txt",
                    mime="text/plain"
                )

            with tab3:
                st.write(
                    "This tool uses document parsing, prompt engineering, and Gemini API integration "
                    "to support CV tailoring and job application preparation."
                )