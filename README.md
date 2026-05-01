# 🤖 Resume Screening AI

An AI-powered Resume Screening System that intelligently ranks candidates based on job descriptions using semantic understanding, experience weighting, and skill matching.

---

## 🚀 Features

- Upload multiple resumes (PDF)
- AI-based semantic matching (Sentence Transformers)
- Experience-based candidate prioritization
- ATS-like scoring system
- Top 3 candidate highlight UI
- Ranked candidate list with match percentage
- Skill match insights

---

## ⚙️ How It Works

1. Extracts text from resumes  
2. Converts text into embeddings using NLP models  
3. Compares resume with job description  
4. Calculates:
   - Semantic similarity  
   - Skill match score  
   - Experience score  
5. Generates final ranking  

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- Sentence Transformers  
- PyTorch  
- Scikit-learn  
- NLP  

---

## ▶️ Installation & Run

```bash
pip install -r requirements.txt
streamlit run app.py

---

## 💾 STEP 3 — Save file

👉 Press **Ctrl + S**

---

## 🚀 STEP 4 — Commit & push

```bash
git add README.md
git commit -m "Fixed README encoding and formatting"
git push
## 📸 Project Screenshots

### 🏠 Home Page
![Home](screenshots/home.png)

### 📤 Resume Upload
![Upload](screenshots/upload.png)

### 📊 Results Dashboard
![Results](screenshots/results.png)