import streamlit as st
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required nltk data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# ---------- STEP 1: Extract Text from PDF ----------
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# ---------- STEP 2: Clean the Text ----------
def clean_text(text):
    text = text.lower()
    
    # Keep C++, C#, .NET type words by replacing + and # temporarily
    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")
    
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word for word in words if word.isalpha() and word not in stop_words]
    return " ".join(cleaned_words)

# ---------- STEP 3: Match Score ----------
def get_match_score(resume_text, job_description):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

# ---------- STEP 4: Missing Skills ----------
def get_missing_skills(resume_text, job_description):
    resume_words = set(clean_text(resume_text).split())
    jd_words = set(clean_text(job_description).split())
    missing = jd_words - resume_words
    return missing

# ---------- UI ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🎯")

st.title("🎯 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to see how well you match!")

st.divider()

# Upload Resume
st.subheader("📄 Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose your resume", type="pdf")

st.divider()

# Job Description
st.subheader("📝 Paste Job Description")
job_description = st.text_area("Paste the job description here", height=200)

st.divider()

# Analyze Button
if st.button("🔍 Analyze"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume first!")
    elif job_description.strip() == "":
        st.warning("⚠️ Please paste a job description!")
    else:
        with st.spinner("Analyzing..."):
            # Extract and analyze
            resume_text = extract_text_from_pdf(uploaded_file)
            score = get_match_score(resume_text, job_description)
            missing_skills = get_missing_skills(resume_text, job_description)

            # Show Match Score
            st.subheader("✅ Match Score")
            if score >= 70:
                st.success(f"🎉 Your resume matches {score}% with this job!")
            elif score >= 40:
                st.warning(f"🙂 Your resume matches {score}% with this job. Some improvements needed.")
            else:
                st.error(f"😟 Your resume matches only {score}%. Consider updating it.")

            # Show progress bar
            st.progress(int(score))

            # Show Missing Skills
            st.subheader("❌ Missing Keywords")
            if missing_skills:
                st.write("These keywords are in the job description but missing from your resume:")
                st.write(", ".join(sorted(missing_skills)))
            else:
                st.success("🎉 No missing keywords!")