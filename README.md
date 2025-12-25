# 📄 AI-Powered Resume Analyzer & CSV Generator

An intelligent resume parsing application that automatically extracts **structured candidate information** from multiple resumes and exports it into a **CSV file**.

This project demonstrates the practical use of **LLMs with LangChain** to convert unstructured resume data into structured, analysis-ready formats.

---

## 🚀 Features

- 📂 Upload a ZIP file containing multiple resumes
- 📄 Supports PDF and DOCX formats
- 🧠 AI-powered structured data extraction
- 📊 Automatic CSV generation
- ⬇️ One-click CSV download
- 🖥️ Simple and clean Streamlit interface

---

## 🧠 Extracted Resume Fields

- Name  
- Email  
- Phone number  
- Skills (list)  
- Experience summary  
- Education  
- LinkedIn profile  
- GitHub profile  

---

## 🏗️ Tech Stack

| Component | Technology |
|--------|------------|
| Frontend | Streamlit |
| AI Orchestration | LangChain |
| LLM | OpenAI (configurable) |
| Data Processing | Pandas |
| File Handling | PyPDF2, python-docx |
| Output | CSV |

---

## 🔄 Workflow

1. Upload a ZIP file containing resumes  
2. System extracts PDF/DOCX files  
3. LLM processes resumes and extracts structured data  
4. Results are displayed in a table  
5. Data is exported as a CSV file  

---

## 🖼️ Application Preview

_Add a screenshot of the Streamlit UI here_

---

## ⚙️ Installation & Setup

```bash
pip install -r requirements.txt
streamlit run app.py
