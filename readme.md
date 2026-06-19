# 🎯 AI Resume Analyzer

An NLP-based tool that analyzes how well your resume matches a job description and identifies missing keywords.

## 🚀 What it Does
- Upload your resume as a PDF
- Paste any job description
- Get a match score (0-100%)
- See missing keywords you should add to your resume

## 🧠 How it Works
1. Extracts text from your PDF resume using PyPDF2
2. Cleans the text by removing stopwords using NLTK
3. Converts both texts into numbers using TF-IDF Vectorization
4. Calculates similarity score using Cosine Similarity
5. Finds missing keywords using set difference

## 🛠️ Tech Stack
- **Language:** Python
- **NLP:** NLTK, scikit-learn
- **UI:** Streamlit
- **PDF Reading:** PyPDF2

## ⚙️ How to Run

**Step 1 - Install libraries:**
```bash
pip install PyPDF2 scikit-learn nltk streamlit
```

**Step 2 - Run the app:**
```bash
streamlit run app.py
```

**Step 3 - Use it:**
- Upload your resume PDF
- Paste a job description
- Click Analyze!