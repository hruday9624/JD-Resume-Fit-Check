import streamlit as st
from docx import Document
import PyPDF2
import google.generativeai as genai  # Correct package for Gemini

# Title of the app
st.title("JD-Resume Fit Check App")

# Retrieve the API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure the Google Generative AI API with your API key
genai.configure(api_key=GOOGLE_API_KEY)

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
    
    # Display a "Generate" button
    if st.button("Generate Match Score"):
        
        st.write("Your resume and job description are being processed...")
        
        # Construct the prompt for analysis
        prompt = f"""
        You are an expert recruiter and hiring manager assistant. Analyze the following details and provide a match score (0-10) for how well the resume matches the job description:

        #1. Analyze this Resume: {resume_text}
        2. Analyze this Job Description: {job_description}
        3. Identify the key skills, experience, and qualifications mentioned in the job description.
        4. Compare the above with the details provided in the resume.
        5. Provide a match score based on how well the resume aligns with the job description. Include a brief justification for the score.
        6. Suggest changes in resume to match the job description.
        7. Suggest some topics for interview preparation.
        """

        # Call the Gemini API (using google-generativeai)
        try:
            # Generate content using the Gemini API (adjust the model name as needed)
            response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
            
            # Parse the response (assuming it's a simple text-based response)
            match_score = response.text.strip().split('\n')[0]  # Get the match score (adjust if response format is different)
            justification = '\n'.join(response.text.strip().split('\n')[1:])  # Get justification (adjust if needed)

            # Display results
            #st.write(f"**Match Score:** {match_score}/10")
            #st.write(f"**Justification:** {justification}")
            st.write(response.text)  # Display the generated response
        
        except Exception as e:
            st.error(f"Error generating match score: {str(e)}")
else:
    st.write("Please upload both a resume and a job description.")

# Add space or content at the bottom
st.write("\n" * 20)  # Adds space to push the content down

# Footer
st.markdown("Built with 🧠 by Hruday & Google Gemini")
