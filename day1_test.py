import os
from parser import extract_text
from model import analyze_resume

job_desc = "python machine learning deep learning flask tensorflow keras"

folder = "resumes"

results = []

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)

        text = extract_text(path)

        analysis = analyze_resume(text, job_desc)

        results.append((file, analysis))

# -------- REMOVE DUPLICATES --------
unique_results = {}
for name, data in results:
    if name not in unique_results:
        unique_results[name] = data
    else:
        if data["percentage"] > unique_results[name]["percentage"]:
            unique_results[name] = data

results = list(unique_results.items())

# -------- SORT --------
results.sort(key=lambda x: x[1]["percentage"], reverse=True)

# -------- PRINT --------
for i, (name, data) in enumerate(results[:10]):
    print(f"\nRank {i+1}: {name}")
    print(f"Score: {data['score']}/5")
    print(f"Match: {data['percentage']}%")
    print(f"Experience: {data['experience']} years")
    print(f"Matched Skills: {', '.join(data['matched_skills'])}")