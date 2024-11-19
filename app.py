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

#Input field for the Resume
st.subheader('Upload your Resume')
# File upload for PDF or DOCX
uploaded_file = st.file_uploader('Upload your Resume (PDF or DOCX)', type=['pdf', 'docx'])

#Input field for the JD
st.subheader('Paste your Job Description here:')
job_description = st.text_input('Job Description', '')

# Handling the uploaded pdf/doc file
if uploaded_file is not None:
    if uploaded_file.type == 'application/pdf':
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = ''
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
        st.text_area('Extracted Resume Text:', extracted_text, height=200)

    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Extract text from DOCX
        doc = Document(uploaded_file)
        extracted_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        st.text_area('Extracted Resume Text:', extracted_text, height=200)
else:
    st.write('Please upload a file to extract the resume text.')