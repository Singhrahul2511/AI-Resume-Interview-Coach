# app.py (Corrected and Final Version)

import streamlit as st
import io
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

# --- Session State Initialization (Cleaned Up) ---
def init_session_state():
    """Initializes all required session state variables."""
    states = {
        'analysis_complete': False, 'score': 0, 'matched_keywords': [],
        'missing_keywords': [], 'resume_bytes': None, 'is_docx': False,
        'edited_resume': None, 'behavioral_questions': None, 'technical_questions': None,
        'interview_started': False, 'interview_questions': [], 'question_index': 0,
        'interview_responses': []
    }
    for key, value in states.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- Social Media Links in Sidebar ---
st.sidebar.title("Connect with the Creator")
st.sidebar.markdown("""
<style>
.social-icons {
    text-align: center;
    padding: 10px;
}
.social-icons a {
    margin: 0 15px;
    color: #4B4B4B; 
    font-size: 24px;
    transition: color 0.3s;
}
.social-icons a:hover {
    color: #007BFF;
}
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

<div class="social-icons">
    <a href="https://github.com/Singhrahul2511" target="_blank"><i class="fab fa-github"></i></a>
    <a href="https://www.linkedin.com/in/rahul-kumar-8ab740268/" target="_blank"><i class="fab fa-linkedin-in"></i></a>
    <a href="https://www.instagram.com/singhrahul2.0/" target="_blank"><i class="fab fa-instagram"></i></a>
</div>
""", unsafe_allow_html=True)


# --- Main Application UI ---
st.title("🚀 AI Resume & Interview Coach")
st.markdown("Optimize your resume and practice for your interview, all in one place!")

uploaded_resume = st.file_uploader("1. Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("2. Paste the Job Description Here", height=250)

if st.button("Analyze Resume & Prepare for Interview", type="primary"):
    if uploaded_resume and job_description:
        with st.spinner("Analyzing..."):
            # Reset states for a new analysis
            init_session_state()
            st.session_state.resume_bytes = io.BytesIO(uploaded_resume.getvalue())
            st.session_state.is_docx = (uploaded_resume.type != "application/pdf")
            st.session_state.resume_bytes.seek(0)
            resume_text = load_docx_text(st.session_state.resume_bytes) if st.session_state.is_docx else load_pdf_text(st.session_state.resume_bytes)

            if "Error" in resume_text:
                st.error(resume_text)
            else:
                matched, missing, job_keywords = compare_resume(resume_text, job_description)
                st.session_state.score = calculate_ats_score(matched, job_keywords)
                st.session_state.matched_keywords = sorted(list(matched))
                st.session_state.missing_keywords = sorted(list(missing))
                st.session_state.analysis_complete = True
    else:
        st.error("Please upload a resume and paste a job description to begin.")

# This is the correct structure: Display the tabs only if analysis is complete
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

        elif st.session_state.question_index < len(st.session_state.interview_questions):
            current_q = st.session_state.interview_questions[st.session_state.question_index]
            q_number = st.session_state.question_index + 1

            st.info(f"**Question {q_number}/{len(st.session_state.interview_questions)}:** {current_q}")

            with st.form(key=f"q_form_{q_number}"):
                answer = st.text_area("Your Answer:", key=f"answer_{q_number}", height=200)
                submitted = st.form_submit_button("Submit Answer")

                if submitted:
                    st.session_state.interview_responses.append({"question": current_q, "answer": answer})
                    st.session_state.question_index += 1
                    st.rerun()

        else:
            st.success("🎉 Mock Interview Complete!")
            st.markdown("Here is a summary of your performance.")

            if st.button("Generate Final Feedback"):
                with st.spinner("AI is analyzing your answers..."):
                    summary = get_final_summary(st.session_state.interview_responses)
                    st.markdown(summary)

            if st.button("Start a New Interview"):
                st.session_state.interview_started = False
                st.session_state.question_index = 0
                st.rerun()

# Note: The old login page router at the end has been completely removed.