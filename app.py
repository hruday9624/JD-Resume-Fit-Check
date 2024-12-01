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
    # Check for minimum content length
    if len(resume_text.strip()) < 100 or len(job_description.strip()) < 100:
        st.error("Please provide more detailed Resume and Job Description.")
        st.stop()

    # Truncate input if too large
    max_input_tokens = 4000  # Example limit
    combined_input = f"{resume_text}\n{job_description}"
    if len(combined_input.split()) > max_input_tokens:
        combined_input = ' '.join(combined_input.split()[:max_input_tokens])
        st.warning("Input text truncated to fit the model's token limit.")

    # Display a "Generate" button
    if st.button("Generate Match Score"):
        st.write("Your resume and job description are being processed...")
        
        # Construct the prompt for analysis
        prompt = f"""
        You are an expert recruiter and hiring manager assistant. Analyze the following details and provide a structured response in the specified format:

        1. Resume: {resume_text}
        2. Job Description: {job_description}

        ### Tasks:
        1. Identify the key skills, experiences, and qualifications mentioned in the Job Description.
        2. Compare the above with the details provided in the Resume.
        3. Provide a match score (out of 10) based on how well the Resume aligns with the Job Description.
        4. Offer a detailed justification for the match score.
        5. Suggest changes to improve the Resume so that it matches the Job Description better.
        6. Recommend relevant topics for interview preparation based on the Job Description.
        
        ### Response Format:
        1. Match Score: [Provide a score out of 10]
        2. Justification: [Provide a detailed analysis of how well the resume matches the job description]
        3. Resume Suggestions: [List actionable changes to align the resume with the job description]
        4. Interview Preparation Topics: [List relevant topics for interview preparation]
        """

        try:

            # Initialize the generative model (adjust model name if needed)
            model = genai.GenerativeModel('gemini-pro')  # Ensure this is the correct model name
            
            # Generate content using the Gemini API
            response = genai.generate_content(
                prompt,
                temperature=0.3,  # Lower temperature for deterministic results
                top_p=0.9,        # Nucleus sampling
                max_output_tokens=500  # Limit response length
            )

            # Ensure response contains text
            if response and hasattr(response, "text"):
                st.write(response.text)  # Display the generated response
            else:
                st.error("No response received from the API.")
        
        except Exception as e:
            st.error(f"API Error: {str(e)}")

else:
    st.write("Please upload both a resume and a job description.")

# Add space or content at the bottom
st.write("\n" * 20)  # Adds space to push the content down

# Footer
st.markdown("Built with 🧠 by Hruday & Google Gemini")
