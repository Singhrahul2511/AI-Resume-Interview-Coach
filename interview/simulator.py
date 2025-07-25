import streamlit as st
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# Use the same LLM initialization as your coach.py
api_key = st.secrets.get("GOOGLE_API_KEY")
llm = None
if api_key:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    except Exception as e:
        print(f"Error initializing Google Gemini model for simulator: {e}")

def generate_interview_questions(job_title):
    """
    Generates a list of behavioral and technical questions for a given job title.
    """
    if not llm:
        st.error("AI model not available. Please ensure your Google API key is configured.")
        return None

    prompt = f"""
    You are an expert hiring manager. For the job title "{job_title}", generate a list of interview questions.
    Provide your response as a single, valid JSON object with two keys: "behavioral_questions" and "technical_questions".
    Each key should have a value that is a list of 5 unique string questions.
    Do not include any other text, explanation, or markdown formatting outside of the JSON object.
    """
    
    try:
        response = llm.invoke(prompt)
        # Clean the response to ensure it's valid JSON
        clean_response = response.content.strip().replace("```json", "").replace("```", "")
        questions = json.loads(clean_response)
        
        # Combine the questions into a single list
        all_questions = questions.get("behavioral_questions", []) + questions.get("technical_questions", [])
        return all_questions
    except (json.JSONDecodeError, AttributeError) as e:
        st.error(f"Failed to parse AI response. The model may have returned an invalid format. Error: {e}")
        return None

def get_final_summary(interview_data):
    """
    Generates a final summary and feedback based on the user's answers.
    """
    if not llm:
        st.error("AI model not available. Please ensure your Google API key is configured.")
        return None

    # Format the questions and answers for the prompt
    qa_pairs_string = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in interview_data])

    prompt = f"""
    You are an expert career coach reviewing a mock interview.
    Based on the following questions and the user's answers, provide a concise summary of their performance.
    Structure your feedback into two sections: "✅ Strengths" and "💡 Areas for Improvement".
    Be constructive and provide specific, actionable advice.

    Interview Transcript:
    ---
    {qa_pairs_string}
    ---
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Failed to generate feedback. Error: {e}")
        return "Could not generate a final summary."