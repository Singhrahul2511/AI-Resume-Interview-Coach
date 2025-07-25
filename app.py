# app.py (Complete Refactored Code with Interview Coach)

import streamlit as st
import io
from auth.db import add_user, get_user_by_email
from auth.auth_utils import hash_password, verify_password
from resume.extractor import load_pdf_text, load_docx_text
from resume.analyzer import compare_resume, calculate_ats_score
from resume.editor import edit_resume_docx
from utils.visualizer import create_ats_pie_chart
from interview.coach import generate_behavioral_questions, generate_technical_questions
from interview.simulator import generate_interview_questions, get_final_summary
# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume & Interview Coach",
    page_icon="🧠",
    layout="wide"
)

# --- Session State Initialization (Includes new interview states) ---
def init_session_state():
    """Initializes all required session state variables."""
    states = {
        'logged_in': False, 'username': "", 'page': "login",
        'analysis_complete': False, 'score': 0, 'matched_keywords': [],
        'missing_keywords': [], 'resume_bytes': None, 'is_docx': False,
        'edited_resume': None, 'behavioral_questions': None, 'technical_questions': None,
        # --- Add these new states for the simulator ---
        'interview_started': False,
        'interview_questions': [],
        'question_index': 0,
        'interview_responses': []
    }
    for key, value in states.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- Authentication Pages ---
def login_page():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = get_user_by_email(email)
            if user and verify_password(password, user['password']):
                st.session_state.logged_in = True
                st.session_state.username = user['name']
                st.rerun()
            else:
                st.error("Invalid email or password.")

def signup_page():
    st.header("Create an Account")
    with st.form("signup_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not all([name, email, password, confirm_password]):
                st.error("Please fill out all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                hashed_pwd = hash_password(password)
                if add_user(name, email, hashed_pwd):
                    st.success("Account created successfully! Please log in.")
                    st.session_state.page = "login"
                    st.rerun()

# --- Main Application ---
def main_app():
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        init_session_state()
        st.rerun()
    
    st.title("🚀 AI Resume & Interview Coach")
    st.markdown("Optimize your resume and practice for your interview, all in one place!")

    uploaded_resume = st.file_uploader("1. Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("2. Paste the Job Description Here", height=250)

    if st.button("Analyze Resume & Prepare for Interview", type="primary"):
        if uploaded_resume and job_description:
            with st.spinner("Analyzing..."):
                st.session_state.resume_bytes = io.BytesIO(uploaded_resume.getvalue())
                st.session_state.is_docx = (uploaded_resume.type != "application/pdf")
                st.session_state.resume_bytes.seek(0)
                resume_text = load_docx_text(st.session_state.resume_bytes) if st.session_state.is_docx else load_pdf_text(st.session_state.resume_bytes)

                if "Error" in resume_text:
                    st.error(resume_text)
                    st.session_state.analysis_complete = False
                    return

                matched, missing, job_keywords = compare_resume(resume_text, job_description)
                st.session_state.score = calculate_ats_score(matched, job_keywords)
                st.session_state.matched_keywords = sorted(list(matched))
                st.session_state.missing_keywords = sorted(list(missing))
                st.session_state.analysis_complete = True
                st.session_state.edited_resume = st.session_state.behavioral_questions = st.session_state.technical_questions = None
        else:
            st.error("Please upload a resume and paste a job description to begin.")
            st.session_state.analysis_complete = False

    if st.session_state.analysis_complete:
        tab1, tab2, tab3 = st.tabs(["📊 ATS & Keyword Analysis", "🧠 Interview Prep Coach", "🤖 AI Interview Simulator"])

        with tab1:
            st.subheader(f"ATS Score: {st.session_state.score:.2f}%")
            col1, col2 = st.columns([1, 2])
            with col1:
                create_ats_pie_chart(st.session_state.score)
            with col2:
                st.markdown("##### Score Improvement Tips")
                st.warning(f"Your resume is missing **{len(st.session_state.missing_keywords)}** key terms. Add them to improve your score.")
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("✅ Matched Keywords"):
                    st.success(", ".join(st.session_state.matched_keywords))
            with col2:
                with st.expander("❌ Missing Keywords"):
                    st.error(", ".join(st.session_state.missing_keywords))

            if st.session_state.is_docx:
                st.markdown("---")
                st.subheader("📥 Get Your Optimized Resume")
                if st.button("Generate Edited Resume"):
                    with st.spinner("Generating..."):
                        edited_stream = edit_resume_docx(st.session_state.resume_bytes, st.session_state.missing_keywords)
                        st.session_state.edited_resume = edited_stream.getvalue() if edited_stream else None
                
                if st.session_state.edited_resume:
                    st.download_button("Download Updated Resume (DOCX)", st.session_state.edited_resume, "optimized_resume.docx")
            else:
                st.info("ℹ️ Resume editing is only available for DOCX files.")

        with tab2:
            st.subheader("Practice for Your Interview")
            st.markdown("Generate potential questions based on your resume and the job description.")

            if st.button("Generate Interview Questions"):
                with st.spinner("AI Coach is thinking..."):
                    st.session_state.resume_bytes.seek(0)
                    resume_text = load_docx_text(st.session_state.resume_bytes) if st.session_state.is_docx else load_pdf_text(st.session_state.resume_bytes)
                    all_skills = st.session_state.matched_keywords + st.session_state.missing_keywords
                    
                    st.session_state.behavioral_questions = generate_behavioral_questions(resume_text)
                    st.session_state.technical_questions = generate_technical_questions(", ".join(all_skills))
            
            if st.session_state.behavioral_questions:
                st.markdown("#### Behavioral Questions")
                st.info("💡 **Tip:** Use the **STAR** method (Situation, Task, Action, Result) to structure your answers.")
                st.markdown(st.session_state.behavioral_questions)
                st.markdown("---")
            
            if st.session_state.technical_questions:
                st.markdown("#### Technical Questions")
                st.markdown(st.session_state.technical_questions)
        with tab3:
            st.subheader("Prepare with a Mock Interview")

            # --- PHASE 1: SETUP ---
            if not st.session_state.interview_started:
                job_title = st.text_input("Enter the Job Title you are applying for (e.g., Data Analyst)", key="job_title_input")

                if st.button("Start Mock Interview"):
                    if job_title:
                        with st.spinner("AI is preparing your questions..."):
                            questions = generate_interview_questions(job_title)
                            if questions:
                                st.session_state.interview_started = True
                                st.session_state.interview_questions = questions
                                st.session_state.question_index = 0
                                st.session_state.interview_responses = []
                                st.rerun()
                    else:
                        st.warning("Please enter a job title to begin.")

            # --- PHASE 2: CONVERSATIONAL LOOP ---
            elif st.session_state.question_index < len(st.session_state.interview_questions):
                current_q = st.session_state.interview_questions[st.session_state.question_index]
                q_number = st.session_state.question_index + 1

                st.info(f"**Question {q_number}/{len(st.session_state.interview_questions)}:** {current_q}")

                with st.form(key=f"q_form_{q_number}"):
                    answer = st.text_area("Your Answer:", key=f"answer_{q_number}", height=200)
                    submitted = st.form_submit_button("Submit Answer")

                    if submitted:
                        # Store the response
                        st.session_state.interview_responses.append({"question": current_q, "answer": answer})
                        # Move to the next question
                        st.session_state.question_index += 1
                        st.rerun()

            # --- PHASE 3: FINAL FEEDBACK ---
            else:
                st.success("🎉 Mock Interview Complete!")
                st.markdown("Here is a summary of your performance.")

                if st.button("Generate Final Feedback"):
                    with st.spinner("AI is analyzing your answers..."):
                        summary = get_final_summary(st.session_state.interview_responses)
                        st.markdown(summary)

                if st.button("Start a New Interview"):
                    # Reset the state to allow a new interview
                    st.session_state.interview_started = False
                    st.session_state.question_index = 0
                    st.rerun()

# --- Page Router ---
if not st.session_state.logged_in:
    st.session_state.page = "login" if st.session_state.page not in ["login", "signup"] else st.session_state.page
    if st.session_state.page == "login":
        login_page()
        if st.button("Don't have an account? Sign Up"):
            st.session_state.page = "signup"; st.rerun()
    elif st.session_state.page == "signup":
        signup_page()
        if st.button("Already have an account? Login"):
            st.session_state.page = "login"; st.rerun()
else:
    # In app.py, at the end of the main_app() function

    st.markdown("---")
    st.markdown("""
    <style>
    .social-icons {
        text-align: center;
        padding: 10px;
    }
    .social-icons a {
        margin: 0 15px;
        color: #4B4B4B; /* Icon color */
        font-size: 24px; /* Icon size */
        transition: color 0.3s;
    }
    .social-icons a:hover {
        color: #007BFF; /* Icon hover color */
    }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <div class="social-icons">
        <a href="https://github.com/Singhrahul2511" target="_blank"><i class="fab fa-github"></i></a>
        <a href="https://www.linkedin.com/in/rahul-kumar-8ab740268/" target="_blank"><i class="fab fa-linkedin-in"></i></a>
        <a href="https://www.instagram.com/singhrahul2.0/" target="_blank"><i class="fab fa-instagram"></i></a>
    </div>
    """, unsafe_allow_html=True)
    main_app()