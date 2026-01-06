import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
import re
import pandas as pd
import urllib.parse

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="ResuMatch AI", layout="wide", page_icon="🚀")

# --- 2. CSS STYLING (Dark Mode Friendly) ---
st.markdown("""
    <style>
    /* BASIC RESET */
    .block-container {
        padding-top: 0rem !important; /* Forces content to top */
        padding-bottom: 5rem;
    
    /* COLORS */
    :root {
        --primary: #3b82f6;
        --secondary: #10b981;
        --dark: #1f2937;
        --card-bg: #1f2937; /* Dark card background */
        --text-color: #ffffff; /* White text for dark mode */
    }

    /* HERO BANNER */
    .hero {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 4rem 1rem 5rem 1rem;
        text-align: center;
        color: white;
        border-radius: 30px;
        margin-top: 1rem;
        margin-left: -5rem; 
        margin-right: -5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 3rem;
    }
    .hero h1 { font-size: 3rem; font-weight: 800; margin: 0; }
    .hero p { opacity: 0.9; margin-top: 10px; font-size: 1.2rem; }

    /* INPUT HEADERS */
    .input-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #9ca3af;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* RESULT CARDS (Dark Theme) */
    .result-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #374151;
        height: 100%;
    }
    .result-card h3 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #60a5fa; /* Light Blue Header */
        margin-top: 0;
        border-bottom: 1px solid #374151;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* TEXT INSIDE CARDS */
    .result-card p, .result-card div, .result-card span, .result-card li {
        color: #e5e7eb; /* Light Grey text */
    }

    /* BUTTON CENTERING WRAPPER */
    .button-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 50px;
        font-weight: 700;
        border: none;
        padding: 0.8rem 3rem;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: transform 0.2s;
    }
    .stButton > button:hover { transform: scale(1.05); }

    /* JOB ITEMS */
    .job-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px;
        background: #111827;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #374151;
    }
    .job-title { font-weight: 600; color: #fff; }
    .job-btn {
        text-decoration: none;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: bold;
        color: white;
        margin-left: 8px;
    }
    .linkedin { background: #0077b5; }
    .google { background: #db4437; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONFIG & FUNCTIONS ---
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else "YOUR_KEY"
genai.configure(api_key=api_key, transport='rest')

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

def get_links(job):
    q = urllib.parse.quote(job)
    return {
        "LI": f"https://www.linkedin.com/jobs/search/?keywords={q}",
        "GL": f"https://www.google.com/search?q={q}+jobs"
    }

# --- 4. HEADER ---
st.markdown("""
    <div class="hero">
        <h1>ResuMatch AI</h1>
        <p>Unlock Your Career Potential — Optimize, Match, and Apply.</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. INPUT SECTION ---
c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.markdown('<div class="input-label">📄 Upload Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

with c2:
    st.markdown('<div class="input-label">💼 Job Description</div>', unsafe_allow_html=True)
    job_desc = st.text_area("JD", height=130, placeholder="Paste JD here...", label_visibility="collapsed")

# CENTERED BUTTON (Using Streamlit Columns hack for perfect center)
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.5, 2, 1.5])
with b2:
    analyze = st.button("🚀 Analyze Match", use_container_width=True)

# --- 6. LOGIC & RESULTS ---
if analyze:
    if uploaded_file and job_desc:
        with st.spinner("Analyzing profile..."):
            try:
                resume_text = input_pdf_text(uploaded_file)
                
                # --- ROBUST PROMPT ---
                # We ask the AI to label sections strictly so we can regex find them
                prompt = f"""
                Act as a Tech Recruiter. Analyze the Resume vs JD.
                
                CRITICAL INSTRUCTION: Output the result in this EXACT format with these headers:
                
                ### SCORE
                [Just the number 0-100]
                
                ### SUMMARY
                [2 sentence summary]
                
                ### KEYWORDS
                [Top 5 missing skills, separated by commas]
                
                ### JOBS
                [Top 3 job titles, separated by commas]
                
                Resume: {resume_text}
                JD: {job_desc}
                """
                
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt).text
                
                # --- SMART PARSING (REGEX) ---
                # This finds text *between* the headers, regardless of formatting
                
                # 1. SCORE
                score_match = re.search(r"### SCORE\s*(\d+)", response)
                score = int(score_match.group(1)) if score_match else 0
                
                # 2. SUMMARY
                summary_match = re.search(r"### SUMMARY\s*(.*?)\s*###", response, re.DOTALL)
                summary = summary_match.group(1).strip() if summary_match else "Analysis Complete."
                
                # 3. KEYWORDS
                kw_match = re.search(r"### KEYWORDS\s*(.*?)\s*###", response, re.DOTALL)
                raw_kw = kw_match.group(1).strip() if kw_match else ""
                keywords = [k.strip() for k in raw_kw.split(',') if k.strip()]
                
                # 4. JOBS
                job_match = re.search(r"### JOBS\s*(.*)", response, re.DOTALL)
                raw_jobs = job_match.group(1).strip() if job_match else ""
                jobs = [j.strip() for j in raw_jobs.split(',') if j.strip()]

                # --- DISPLAY GRID ---
                st.markdown("<hr style='border-color: #374151; margin: 2rem 0;'>", unsafe_allow_html=True)
                
                # ROW 1
                rc1, rc2 = st.columns([1, 1.5], gap="large")
                
                with rc1:
                    color = "#10b981" if score >= 70 else "#f59e0b" if score >= 50 else "#ef4444"
                    st.markdown(f"""
                        <div class="result-card" style="text-align:center;">
                            <h3>🎯 Match Score</h3>
                            <div style="font-size:4rem; font-weight:800; color:{color};">{score}%</div>
                            <p style="margin-top:10px;">{summary}</p>
                        </div>
                    """, unsafe_allow_html=True)

                with rc2:
                    st.markdown('<div class="result-card"><h3>📊 Keyword Gap</h3>', unsafe_allow_html=True)
                    if keywords:
                        # Create valid data for graph
                        data = {"Skill": keywords[:5], "Gap Impact": [90, 80, 70, 60, 50][:len(keywords)]}
                        df = pd.DataFrame(data)
                        st.bar_chart(df.set_index("Skill"), color=color, height=200)
                    else:
                        st.success("No critical gaps found!")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ROW 2
                rc3, rc4 = st.columns([1.5, 1], gap="large")
                
                with rc3:
                    st.markdown('<div class="result-card"><h3>⚠️ Skills to Add</h3>', unsafe_allow_html=True)
                    if keywords:
                        for k in keywords[:5]:
                            st.markdown(f"<li style='margin-bottom:5px;'>{k}</li>", unsafe_allow_html=True)
                    else:
                        st.write("Resume optimized.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with rc4:
                    st.markdown('<div class="result-card"><h3>💼 Job Matches</h3>', unsafe_allow_html=True)
                    if jobs:
                        for job in jobs[:3]:
                            links = get_links(job)
                            st.markdown(f"""
                                <div class="job-item">
                                    <div class="job-title">{job}</div>
                                    <div>
                                        <a href="{links['LI']}" target="_blank" class="job-btn linkedin">In</a>
                                        <a href="{links['GL']}" target="_blank" class="job-btn google">G</a>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No job titles found.")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")
                # Debugging: show raw response if parsing fails
                # st.write(response) 
    else:
        st.warning("Please upload a resume and provide a job description.")