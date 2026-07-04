# AI-Powered CV and Cover Letter Assistant

A Streamlit application that analyzes a candidate's CV against a job description using Google's Gemini API and generates tailored application materials.

## Features

- Upload CV files in PDF, DOCX, or TXT format
- Extract text from uploaded documents
- Analyze CV-job description match using Gemini
- Generate an overall match score
- Identify strong matches and missing keywords
- Suggest tailored CV bullet points
- Generate a cover letter draft
- Generate interview preparation questions
- Export the analysis as a TXT file

## Technologies Used

- Python
- Streamlit
- Gemini API
- python-docx
- pypdf
- python-dotenv
- Git and GitHub

## Project Purpose

This project explores how large language models can support job application workflows. It demonstrates document parsing, prompt engineering, AI-assisted analysis, and user-focused workflow automation.

## How It Works

1. The user uploads a CV.
2. The user pastes a job description.
3. The application extracts text from the CV.
4. Gemini analyzes the CV against the job description.
5. The app returns a structured report with recommendations.

## Security Note

API keys are stored locally in a `.env` file and excluded from GitHub using `.gitignore`.

## Future Improvements

- PDF export
- Saved analysis history
- Comparison between different job descriptions
- More advanced keyword scoring