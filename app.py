import streamlit as st
from parser import extract_text
from model import analyze_resume
import os

st.set_page_config(
    page_title="Resume Screening AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- GLOBAL STYLE ----------
st.markdown(""" 
<style>
/* (KEEPING YOUR FULL CSS EXACTLY SAME — no changes) */
.stApp {
    background: radial-gradient(circle at top left, #5b4bff 0, #2b0f73 40%, #050017 100%);
    font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1200px; }
.main-title { text-align: center; font-size: 40px; font-weight: 700; color: #ffffff; }
.sub-text { text-align: center; font-size: 16px; color: #c0c0ff; margin-bottom: 2rem; }
.glass-card {
    background: rgba(15, 8, 60, 0.8);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.65);
}
.top-main-card {
    background: linear-gradient(145deg, rgba(9,9,121,0.98), rgba(115,78,255,0.98));
    border-radius: 28px;
    padding: 26px;
    color: white;
}
.small-card {
    background: rgba(10,3,40,0.4);
    border-radius: 22px;
    padding: 18px;
    text-align:center;
}
.circular-wrapper {
    width:130px;height:130px;border-radius:50%;
    background:conic-gradient(#00ffb3 var(--deg), #2b184b 0);
    display:flex;align-items:center;justify-content:center;
}
.circular-inner {
    width:96px;height:96px;border-radius:50%;
    background:#08011b;color:white;
    display:flex;align-items:center;justify-content:center;
}
.avatar-circle {
    width:58px;height:58px;border-radius:50%;
    background: radial-gradient(circle at 30% 10%, #ffd194, #ff6a88);
    display:flex;align-items:center;justify-content:center;
}
.recommend-pill {
    padding:8px 18px;border-radius:999px;
    background:#00e29b;color:#052326;
}
.robot-card {
    background: rgba(7,1,30,0.9);
    border-radius:26px;
    padding:22px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">Resume Screening AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Smart candidate matching powered by AI</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
col1, col2 = st.columns([1.3,1])

with col1:
    job_desc = st.text_area("Job Description")

with col2:
    uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)

analyze_clicked = st.button("Analyze Candidates 🚀")

# ---------- ANALYSIS ----------
if analyze_clicked:

    results = []

    for file in uploaded_files:
        file_path = file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        text = extract_text(file_path)

        if text:
            analysis = analyze_resume(text, job_desc)
            results.append((file.name, analysis))

        os.remove(file_path)

    if results:

        # ✅ REMOVE DUPLICATES
        unique_results = {}
        for name, data in results:
            if name not in unique_results:
                unique_results[name] = data
            else:
                if data["percentage"] > unique_results[name]["percentage"]:
                    unique_results[name] = data

        results = list(unique_results.items())

        # ✅ SORT
        results.sort(key=lambda x: x[1]["percentage"], reverse=True)

        # ---------- TOP SECTION ----------
        main_col, side_col = st.columns([2,1])

        with main_col:
            left_small, center_main, right_small = st.columns([1,1.4,1])

            # LEFT (3rd)
            if len(results) >= 3:
                name_l, data_l = results[2]
                with left_small:
                    st.markdown(f"""
                    <div class="small-card">
                        <div class="circular-wrapper" style="--deg:{data_l['percentage']*3.6}deg;">
                            <div class="circular-inner">{data_l['percentage']}%</div>
                        </div>
                        <div class="avatar-circle">{name_l[0]}</div>
                        <div>{data_l['experience']} yrs exp</div>
                    </div>
                    """, unsafe_allow_html=True)

            # CENTER (TOP)
            top_name, top_data = results[0]
            with center_main:
                st.markdown(f"""
                <div class="top-main-card">
                    <h3>Best Match</h3>
                    <div class="circular-wrapper" style="--deg:{top_data['percentage']*3.6}deg;">
                        <div class="circular-inner">{top_data['percentage']}%</div>
                    </div>
                    <div class="avatar-circle">{top_name[0]}</div>
                    <h4>{top_name}</h4>
                    <p>Score: {top_data['score']} / 5</p>
                    <p>Experience: {top_data['experience']} yrs</p>
                    <span class="recommend-pill">Recommended</span>
                </div>
                """, unsafe_allow_html=True)

            # RIGHT (2nd)
            if len(results) >= 2:
                name_r, data_r = results[1]
                with right_small:
                    st.markdown(f"""
                    <div class="small-card">
                        <div class="circular-wrapper" style="--deg:{data_r['percentage']*3.6}deg;">
                            <div class="circular-inner">{data_r['percentage']}%</div>
                        </div>
                        <div class="avatar-circle">{name_r[0]}</div>
                        <div>{data_r['experience']} yrs exp</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ---------- LIST ----------
        st.markdown("### Ranked Candidates")

        for i, (name, data) in enumerate(results[:10]):
            st.write(f"#{i+1} {name} | {data['percentage']}% | {data['experience']} yrs")
            st.progress(data['percentage']/100)