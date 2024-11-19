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

# Ensure both resume and JD are provided before proceeding
if resume_text and job_description:
    st.write("Your resume and job description are being processed...")
    
    # Call the generative AI API or process the match logic here (e.g., calling the Gemini API)
    # For now, we simulate the match process and display the output
    
    prompt = f"""
    You are an expert recruiter and hiring manager assistant. Analyze the following details and provide a match score (0-10) for how well the resume matches the job description:

    1. Analyze this Resume: {resume_text}
    2. Analyze this Job Description: {job_description}
    3. Identify the key skills, experience, and qualifications mentioned in the job description.
    4. Compare the above with the details provided in the resume.
    5. Provide a match score based on how well the resume aligns with the job description. Include a brief justification for the score.
    """

    # Here you would send the 'prompt' to the API or some function to generate a result
    # For now, we'll simulate a result:
    match_score = 8  # Just an example score
    justification = "The resume matches most of the key skills mentioned in the job description, but there is some mismatch in the experience level."

    # Display results
    st.write(f"**Match Score:** {match_score}/10")
    st.write(f"**Justification:** {justification}")

else:
    st.write("Please upload both a resume and a job description.")
