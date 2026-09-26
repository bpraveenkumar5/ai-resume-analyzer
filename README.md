# AI Resume Analyzer

AI Resume Analyzer is a Streamlit web application that reads a candidate's resume PDF, compares it to a target job role, and provides AI-powered feedback on skills, strengths, gaps, suggestions, and interview preparation.

## Overview

This app helps job seekers and recruiters quickly evaluate whether a resume matches a specific role. It extracts text from the uploaded PDF, sends the content to Groq's AI model, and returns a structured analysis with:

- Candidate summary
- Relevant skills
- Strengths
- Missing or weak skills
- Resume improvement suggestions
- Interview preparation topics

## Features

- Upload resume in PDF format
- Input the target job role
- Extract text from the resume automatically
- Analyze resume against the requested role
- View structured AI recommendations
- Simple, user-friendly Streamlit interface

## Tech Stack

- Python
- Streamlit
- pypdf
- Python-dotenv
- Groq API

## Prerequisites

Before running the project, make sure you have:

- Python 3.9 or newer
- pip installed
- A Groq API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/bpraveenkumar5/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

If you deploy the app, you can also store the key in Streamlit secrets using the same key name: `GROQ_API_KEY`.

## Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal in your browser.

## Usage

1. Upload a resume in PDF format.
2. Enter the target job role, for example: `Java Developer`.
3. Click the Analyze Resume button.
4. Review the AI-generated summary, skills, strengths, missing skills, suggestions, and interview guidance.

## Notes

- The app expects a text-based PDF file.
- It analyzes only the content present in the PDF and does not invent missing experience or skills.
- The app relies on the Groq API for analysis, so a valid API key is required.

## Project Structure

```text
ai-resume-analyzer/
├── app.py
├── requirements.txt
├── .env
├── README.md
└── venv/
```

## License

This project is provided for educational and personal use. Add a license if you plan to share or publish it publicly.
