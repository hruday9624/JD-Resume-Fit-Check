import streamlit as st
import google.generativeai as genai

from docx import Document  # To handle .docx files
import PyPDF2  # To handle .pdf files

# App header
st.header("JD-Resume-Fit-Check")

# Retrieve the API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure the Google Generative AI API with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# Input field for the medicine name
st.subheader("Enter Medicine Details:")
medicine_name = st.text_input('Medicine Name', '')

#Input field for the Resume
st.subheader('Upload your Resume')
# File upload for PDF or DOCX
uploaded_file = st.file_uploader('Upload your Resume (PDF or DOCX)', type=['pdf', 'docx'])