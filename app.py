import streamlit as st
from docx import Document
import PyPDF2

# Title of the app
st.title("JD-Resume Fit Check App")

# Create two columns
col1, col2 = st.columns(2)

# Left column: Resume upload
with col1:
    st.subheader('Upload your Resume')
    uploaded_file = st.file_uploader('Upload your Resume (PDF or DOCX)', type=['pdf', 'docx'])
    resume_text = ""
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            st.success("Resume uploaded and processed!")
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            # Extract text from DOCX
            doc = Document(uploaded_file)
            resume_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            st.success("Resume uploaded and processed!")

# Right column: JD input
with col2:
    st.subheader('Paste your Job Description')
    job_description = st.text_area('Enter Job Description', '', height=150)
    if job_description:
        st.success("Job Description received!")

# Bottom section: Output
st.subheader("Fit Check Results")
if resume_text and job_description:
    st.write("Your resume and job description are being processed...")
    # Placeholder for processing logic
    st.write("Results will be displayed here.")
else:
    st.write("Please upload both a resume and a job description.")
