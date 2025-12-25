import streamlit as st
import zipfile
import os
import tempfile
import pandas as pd
from typing import List, Optional

from PyPDF2 import PdfReader
import docx

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


# -----------------------------
# 1. Structured Output Schema
# -----------------------------
response_schemas = [
    ResponseSchema(name="name", description="Candidate full name"),
    ResponseSchema(name="email", description="Email address"),
    ResponseSchema(name="phone", description="Phone number"),
    ResponseSchema(name="skills", description="List of skills"),
    ResponseSchema(name="experience_summary", description="Short experience summary"),
    ResponseSchema(name="education", description="Education details"),
    ResponseSchema(name="linkedin", description="LinkedIn profile URL"),
    ResponseSchema(name="github", description="GitHub profile URL"),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)


# -----------------------------
# 2. Resume Readers
# -----------------------------
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


# -----------------------------
# 3. ZIP Extraction
# -----------------------------
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


# -----------------------------
# 4. LangChain Resume Parser
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = PromptTemplate(
    template="""
You are an AI resume analyzer.

Extract the following information from the resume text.
If a field is missing, return null.
Skills must be returned as a list of strings.

{format_instructions}

Resume Text:
{resume_text}
""",
    input_variables=["resume_text"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        resume_text = read_pdf(file_path)
    elif file_path.endswith(".docx"):
        resume_text = read_docx(file_path)
    else:
        return None

    chain = prompt | llm | parser
    return chain.invoke({"resume_text": resume_text})


# -----------------------------
# 5. Process All Resumes
# -----------------------------
def process_resumes(folder_path):
    results = []

    for file in os.listdir(folder_path):
        if file.lower().endswith((".pdf", ".docx")):
            file_path = os.path.join(folder_path, file)
            parsed_data = parse_resume(file_path)
            if parsed_data:
                results.append(parsed_data)

    return results


# -----------------------------
# 6. Streamlit UI
# -----------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI-Powered Resume Analyzer & CSV Generator")

st.write(
    "Upload a ZIP file containing multiple resumes (PDF or DOCX). "
    "The system will extract structured information and generate a CSV file."
)

uploaded_zip = st.file_uploader(
    "Upload ZIP File",
    type=["zip"]
)

if uploaded_zip:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "resumes.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        extract_zip(zip_path, tmpdir)

        with st.spinner("Analyzing resumes using AI..."):
            resume_data = process_resumes(tmpdir)

        if resume_data:
            df = pd.DataFrame(resume_data)

            st.success("Resume analysis completed successfully")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="resume_analysis.csv",
                mime="text/csv"
            )
        else:
            st.warning("No valid resumes found in the ZIP file.")
