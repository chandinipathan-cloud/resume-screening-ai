from sentence_transformers import SentenceTransformer, util
import re

# Load model once (VERY IMPORTANT)
model = SentenceTransformer('all-MiniLM-L6-v2')


# -------- EXPERIENCE --------
def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    years = 0
    for m in matches:
        years = max(years, int(m[0]))
    return years


# -------- SECTION SPLITTING --------
def extract_sections(text):

    text = text.lower()

    sections = {
        "skills": "",
        "experience": "",
        "projects": ""
    }

    if "skills" in text:
        sections["skills"] = text.split("skills")[-1][:500]

    if "experience" in text:
        sections["experience"] = text.split("experience")[-1][:700]

    if "project" in text:
        sections["projects"] = text.split("project")[-1][:700]

    return sections


# -------- SEMANTIC SIMILARITY --------
def semantic_score(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2)[0][0])


# -------- MAIN FUNCTION --------
def analyze_resume(resume_text, job_desc):

    sections = extract_sections(resume_text)

    # 🔥 semantic scoring
    skill_score = semantic_score(sections["skills"], job_desc)
    exp_score = semantic_score(sections["experience"], job_desc)
    proj_score = semantic_score(sections["projects"], job_desc)

    # experience years boost
    years = extract_experience(resume_text)
    exp_boost = min(years * 0.05, 0.3)

    # 🎯 FINAL WEIGHTED SCORE
    final = (
        skill_score * 0.4 +
        exp_score * 0.3 +
        proj_score * 0.2 +
        exp_boost
    )

    final = min(final, 1)

    percentage = round(final * 100, 2)
    score = round(final * 5)

    # -------- INSIGHTS --------
    insights = []

    if skill_score > 0.5:
        insights.append("Strong skill alignment")

    if years >= 3:
        insights.append(f"{years}+ years experience")

    if proj_score > 0.4:
        insights.append("Relevant projects")

    if not insights:
        insights.append("Moderate fit")

    return {
        "score": score,
        "percentage": percentage,
        "experience": years,
        "matched_skills": [],  # semantic now, so optional
        "insight": ", ".join(insights)
    }