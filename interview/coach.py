import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# --- This section is now safe as it contains no Streamlit commands ---
api_key = st.secrets.get("GOOGLE_API_KEY")

llm = None
# Initialize the LLM only if the API key exists
if api_key:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    except Exception as e:
        # We'll show the error later, inside the function call
        print(f"Error initializing Google Gemini model: {e}")
# --- End of safe section ---


def generate_behavioral_questions(resume_text):
    """Generates behavioral questions based on resume content."""
    # --- The check and Streamlit command are now safely inside the function ---
    if not llm:
        st.warning("Google API key not found or failed to initialize. Please configure it in your secrets to use this feature.")
        return "Language model not available."

    prompt = f"""
    You are an AI assistant acting as a hiring manager for a student internship.
    Based on the following resume text, generate 5 detailed behavioral interview questions.
    Resume Text:
    ---
    {resume_text}
    ---
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return "An error occurred while communicating with the AI model."

def generate_technical_questions(skills_text):
    """Generates technical questions based on a list of skills."""
    # --- The check and Streamlit command are now safely inside the function ---
    if not llm:
        st.warning("Google API key not found or failed to initialize. Please configure it in your secrets to use this feature.")
        return "Language model not available."
        
    prompt = f"""
    You are an AI assistant acting as a senior engineer conducting a technical screen.
    Based on the following skills, generate 5 technical questions for a student.
    Skills:
    ---
    {skills_text}
    ---
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return "An error occurred while communicating with the AI model."