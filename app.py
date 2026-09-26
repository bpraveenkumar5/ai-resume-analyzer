import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from groq import Groq
import os
import json


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)


# =========================================================
# 2. LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================================
# 3. CHECK API KEY
# =========================================================

if not GROQ_API_KEY:
    st.error("Groq API key is not configured.")
    st.info("Please add GROQ_API_KEY to your .env file.")
    st.stop()


# =========================================================
# 4. CREATE GROQ CLIENT
# =========================================================

client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# 5. APPLICATION UI
# =========================================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and get AI-powered feedback "
    "on your skills, strengths, weaknesses, and interview preparation."
)


# =========================================================
# 6. RESUME UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


# =========================================================
# 7. TARGET JOB ROLE
# =========================================================

job_role = st.text_input(
    "Target Job Role",
    placeholder="Example: Java Developer"
)


# =========================================================
# 8. ANALYZE BUTTON
# =========================================================

if st.button("🔍 Analyze Resume"):

    # -----------------------------------------------------
    # Validate resume upload
    # -----------------------------------------------------

    if uploaded_file is None:
        st.warning("Please upload your resume first.")
        st.stop()


    # -----------------------------------------------------
    # Validate target job role
    # -----------------------------------------------------

    if job_role.strip() == "":
        st.warning("Please enter the target job role.")
        st.stop()


    # -----------------------------------------------------
    # Extract text from PDF
    # -----------------------------------------------------

    try:

        pdf_reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"


    except Exception as e:

        st.error("Unable to read the PDF file.")
        st.error(str(e))
        st.stop()


    # -----------------------------------------------------
    # Check extracted text
    # -----------------------------------------------------

    if resume_text.strip() == "":
        st.error(
            "Could not extract text from this PDF. "
            "Please upload a text-based PDF."
        )
        st.stop()


    # -----------------------------------------------------
    # Show extraction success
    # -----------------------------------------------------

    st.success("Resume uploaded and text extracted successfully!")


    # -----------------------------------------------------
    # Optional: Display extracted resume text
    # -----------------------------------------------------

    with st.expander("📄 View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            resume_text,
            height=400
        )


    # =====================================================
    # 9. CREATE AI PROMPT
    # =====================================================

    prompt = f"""
Analyze this resume for the target job role.

Target Job Role:
{job_role}

Resume:
{resume_text}

Provide:

1. A concise candidate summary.
2. Relevant technical and professional skills found in the resume.
3. Candidate strengths.
4. Skills that appear missing or weak for the target job role.
5. Practical resume improvement suggestions.
6. Interview preparation topics.

Important instructions:

- Base your analysis only on information present in the resume.
- Do not invent experience.
- Do not invent skills.
- Do not invent projects.
- Do not invent certifications.
- Do not invent qualifications.
- Compare the resume against the target job role.
"""


    # =====================================================
    # 10. CALL GROQ
    # =====================================================

    try:

        with st.spinner("🤖 AI is analyzing your resume..."):

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an experienced technical recruiter "
                            "and resume reviewer."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "resume_analysis",

                        "schema": {

                            "type": "object",

                            "properties": {

                                "summary": {
                                    "type": "string"
                                },

                                "skills": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },

                                "strengths": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },

                                "missing_skills": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },

                                "suggestions": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },

                                "interview_preparation": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },

                            "required": [
                                "summary",
                                "skills",
                                "strengths",
                                "missing_skills",
                                "suggestions",
                                "interview_preparation"
                            ],

                            "additionalProperties": False
                        }
                    }
                }
            )


        # =================================================
        # 11. GET AI RESPONSE
        # =================================================

        analysis_text = response.choices[0].message.content


        # =================================================
        # 12. CONVERT JSON STRING TO PYTHON DICTIONARY
        # =================================================

        analysis = json.loads(analysis_text)


    except json.JSONDecodeError:

        st.error(
            "The AI returned an unexpected response format."
        )

        st.stop()


    except Exception as e:

        st.error(
            "Something went wrong while analyzing the resume."
        )

        st.error(str(e))

        st.stop()


    # =====================================================
    # 13. DISPLAY ANALYSIS
    # =====================================================

    st.success("🎉 Resume analysis completed!")


    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    st.subheader("📋 Resume Summary")

    st.write(
        analysis["summary"]
    )


    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    st.subheader("💻 Relevant Skills")

    for skill in analysis["skills"]:

        st.write(
            f"✅ {skill}"
        )


    # -----------------------------------------------------
    # Strengths
    # -----------------------------------------------------

    st.subheader("💪 Strengths")

    for strength in analysis["strengths"]:

        st.write(
            f"• {strength}"
        )


    # -----------------------------------------------------
    # Missing Skills
    # -----------------------------------------------------

    st.subheader("⚠️ Missing or Weak Skills")

    for skill in analysis["missing_skills"]:

        st.write(
            f"• {skill}"
        )


    # -----------------------------------------------------
    # Suggestions
    # -----------------------------------------------------

    st.subheader("🚀 Suggestions for Improvement")

    for suggestion in analysis["suggestions"]:

        st.write(
            f"• {suggestion}"
        )


    # -----------------------------------------------------
    # Interview Preparation
    # -----------------------------------------------------

    st.subheader("🎯 Interview Preparation")

    for topic in analysis["interview_preparation"]:

        st.write(
            f"• {topic}"
        )