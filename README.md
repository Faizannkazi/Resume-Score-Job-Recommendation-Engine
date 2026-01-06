#  ResumeMatch AI: Smart Resume Scorer & Job Recommender

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini%20AI-8E75B2?style=for-the-badge&logo=google%20bard&logoColor=white)

**ResumeMatch AI** is an intelligent Applicant Tracking System (ATS) simulator designed to help job seekers optimize their resumes. By leveraging Google's Gemini Pro model, it analyzes resumes against job descriptions in real-time, providing a match score, missing keywords, and tailored job recommendations.

🔗 **Live Demo:** [Click here to view the App](ats-resume-matching-system.streamlit.app) 

---

##  Key Features

* **📄 PDF Resume Parsing:** Extracts text from PDF resumes using `PyPDF2`.
* **🤖 AI-Powered Analysis:** Uses Google Gemini (Generative AI) to act as a Tech Recruiter and evaluate candidate relevance.
* **📊 Smart Scoring System:** Provides a percentage match score (0-100%) indicating how well the resume fits the job description.
* **🔍 Keyword Gap Analysis:** Identifies specific hard/soft skills missing from the resume.
    * *Toggle View:* Switch between a data table and a visual bar chart.
* **💼 Job Recommendations:** Suggests relevant job titles based on the profile and provides direct search links (LinkedIn, Google Jobs).
* **🌑 Dark Mode Friendly:** Fully styled UI for a modern, professional look.

---

##  Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Engine:** [Google Gemini API](https://ai.google.dev/)
* **Data Handling:** Pandas, Regex
* **PDF Processing:** PyPDF2

---

##  Installation & Local Setup

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Faizannkazi/Resume-Score-Job-Recommendation-Engine.git](https://github.com/Faizannkazi/Resume-Score-Job-Recommendation-Engine.git)
    cd Resume-Score-Job-Recommendation-Engine
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys:**
    * Create a file named `.streamlit/secrets.toml` in the root directory.
    * Add your Google Gemini API key:
        ```toml
        GEMINI_API_KEY = "your_actual_api_key_here"
        ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

##  How It Works

1.  **Upload:** User uploads their resume in PDF format.
2.  **Paste:** User pastes the Job Description (JD) for the role they are targeting.
3.  **Analyze:** The app sends both texts to the Gemini AI model with a custom prompt engineering structure.
4.  **Results:** The AI returns a structured JSON-like response containing the score, summary, and missing keywords, which the app parses and displays.



---

*Star ⭐️ this repo if you found it useful!*
