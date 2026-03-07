# Cybersecurity Risk Assessment Tool
# Copyright (c) 2026 David Zilberman
# Licensed under the MIT License

import streamlit as st
import sqlite3
import datetime
import plotly.graph_objects as go
from questions import questions
import pandas as pd
from report_generator import generate_report
import os
import json
import hashlib

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Cybersecurity Risk Assessment Tool",
    initial_sidebar_state="expanded"
)

# -------------------------
# DATABASE CONNECTION
# -------------------------

conn = sqlite3.connect("cyber_risk.db", check_same_thread=False)
cursor = conn.cursor()

with open("database.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()

# -------------------------
# LOAD CSS
# -------------------------

def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# -------------------------
# SESSION STATE
# -------------------------

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "finished" not in st.session_state:
    st.session_state.finished = False

if "industry_confirmed" not in st.session_state:
    st.session_state.industry_confirmed = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

if "results_saved" not in st.session_state:
    st.session_state.results_saved = False

if "report_path" not in st.session_state:
    st.session_state.report_path = ""

# -------------------------
# HEADER AND TITLE
# -------------------------
st.title("Cybersecurity Risk Assessment Tool")

# -------------------------
# USER STORAGE
# -------------------------

SAVED_JSONS_DIR = os.path.join(os.path.dirname(__file__), "Saved JSONs")
os.makedirs(SAVED_JSONS_DIR, exist_ok=True)
USERS_FILE = os.path.join(SAVED_JSONS_DIR, "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# RISK SCORE HISTORY (JSON)
# -------------------------

def save_risk_score(username, company, industry, total, categories, email="", report_path=""):
    users = load_users()
    if username not in users:
        return

    if "history" not in users[username]:
        users[username]["history"] = []

    users[username]["history"].append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company": company,
        "industry": industry,
        "email": email if email else "Not provided",
        "total_score": round(total, 2),
        "categories": {k: round(v, 2) for k, v in categories.items()},
        "report_path": report_path
    })

    save_users(users)

def get_user_risk_history(username):
    users = load_users()
    if username not in users:
        return []
    return users[username].get("history", [])

def display_risk_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Risk Score History")

    history = get_user_risk_history(st.session_state["username"])

    if not history:
        st.sidebar.info("No history yet.")
        return

    for i, entry in enumerate(reversed(history)):
        with st.sidebar.expander(f"{entry['company']} — {entry['date']}"):
            st.write(f"**Industry:** {entry['industry']}")
            st.write(f"**Email:** {entry.get('email', 'Not provided')}")
            st.write(f"**Total Score:** {entry['total_score']}")
            st.write("**Categories:**")
            for category, score in entry["categories"].items():
                st.write(f"- {category}: {score}")

            # Show download button if report file still exists
            report_path = entry.get("report_path", "")
            if report_path and os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    st.download_button(
                        label="Download Report",
                        data=f.read(),
                        file_name=os.path.basename(report_path),
                        mime="application/pdf",
                        key=f"download_{i}"
                    )
            else:
                st.caption("Report file not available")

# -------------------------
# AUTH FUNCTIONS
# -------------------------

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")

    if st.sidebar.button("Login", key="login_submit"):
        users = load_users()
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

def register():
    st.sidebar.title("Register")
    new_username = st.sidebar.text_input("Choose a Username", key="reg_username")
    new_password = st.sidebar.text_input("Choose a Password", type="password", key="reg_password")
    confirm_password = st.sidebar.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.sidebar.button("Register", key="register_submit"):
        if not new_username or not new_password:
            st.sidebar.error("Username and password cannot be empty")
        elif new_password != confirm_password:
            st.sidebar.error("Passwords do not match")
        else:
            users = load_users()
            if new_username in users:
                st.sidebar.error("Username already exists")
            else:
                users[new_username] = {
                    "password": hash_password(new_password),
                    "history": []
                }
                save_users(users)
                st.sidebar.success("Account created! Please log in.")

def logout():
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.rerun()
        
# -------------------------
# LOGIN GATE
# -------------------------

if not st.session_state.get("logged_in", False):

    st.sidebar.markdown("### Please Select Option:")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("Login", key="tab_login", use_container_width=True):
            st.session_state.auth_mode = "Login"
            st.rerun()
    with col2:
        if st.sidebar.button("Register", key="tab_register", use_container_width=True):
            st.session_state.auth_mode = "Register"
            st.rerun()

    if st.session_state.auth_mode == "Login":
        login()
    else:
        register()

    st.warning("Please log in to access the app.")
    st.stop()

else:
    logout()
    display_risk_history()



# -------------------------
# CONSENT & EMAIL
# -------------------------

consent = st.checkbox(
    "I consent to anonymous data being used for cybersecurity trend analysis."
)

if not consent:
    st.warning("Consent required to run assessment.")
    st.stop()

email = st.text_input("Email (optional)")

if email:
    import re
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        st.error("Please enter a valid email address (e.g. name@example.com)")
        st.stop()

# -------------------------
# COMPANY NAME
# -------------------------

company = st.text_input("Company Name")

if company:
    st.success(f"Welcome {company}")

# -------------------------
# INDUSTRY
# -------------------------

INDUSTRY_MULTIPLIERS = {
    "General": 1.0,
    "Finance": 1.3,
    "Healthcare": 1.4,
    "Retail": 1.2
}

if company and not st.session_state.industry_confirmed:
    industry = st.selectbox(
        "Industry",
        ["General", "Finance", "Healthcare", "Retail"]
    )

    if st.button("Confirm Industry", key="confirm_industry_btn"):
        st.session_state.industry = industry
        st.session_state.industry_confirmed = True
        st.rerun()

# -------------------------
# HELPER FUNCTIONS
# -------------------------

def get_db_risk_history():
    cursor.execute("""
    SELECT completed_at, total_score
    FROM assessments
    ORDER BY completed_at
    """)
    rows = cursor.fetchall()
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["Date", "Risk Score"])
    return df

def get_industry_scores(industry):
    cursor.execute("""
    SELECT total_score
    FROM assessments
    JOIN users ON users.id = assessments.user_id
    WHERE users.industry = ?
    """, (industry,))
    rows = cursor.fetchall()
    return [r[0] for r in rows]

# -------------------------
# QUESTIONS
# -------------------------

if company and st.session_state.industry_confirmed:

    industry = st.session_state.industry

    st.subheader(f"{company}'s Risk Assessment ({industry})")

    if not st.session_state.finished:

        progress = st.session_state.current_q / len(questions)
        st.progress(progress)

        q = questions[st.session_state.current_q]

        st.markdown(
            f"<div class='custom-card'>{q['question']}</div>",
            unsafe_allow_html=True
        )

        answer = st.radio(
            "",
            ["Yes", "No"],
            index=None,
            key=f"radio_{st.session_state.current_q}"
        )

        if st.button("Submit", key="submit_answer"):
            if answer is None:
                st.warning("Please select an answer.")
            else:
                answer_value = 0 if answer == "Yes" else 1
                st.session_state.responses[q["id"]] = answer_value

                if st.session_state.current_q < len(questions) - 1:
                    st.session_state.current_q += 1
                else:
                    st.session_state.finished = True
                    st.session_state.results_saved = False
                    st.session_state.report_path = ""
                    st.session_state.ai_advice = "" 

                st.rerun()

    # -------------------------
    # RESULTS
    # -------------------------

    else:

        multiplier = INDUSTRY_MULTIPLIERS[industry]

        total = 0
        categories = {}

        for q in questions:
            q_score = q["weight"] * st.session_state.responses.get(q["id"], 0)
            q_score *= multiplier
            total += q_score

            if q["category"] not in categories:
                categories[q["category"]] = 0
            categories[q["category"]] += q_score

        if total < 50:
            risk_label = "Low"
        elif total < 100:
            risk_label = "Moderate"
        else:
            risk_label = "High"

        # -------------------------
        # SAVE TO DATABASE + REPORT (once only)
        # -------------------------

        if not st.session_state.results_saved:

            cursor.execute(
                """
                INSERT INTO users (company_name, industry, consent, email, created_at)
                VALUES (?,?,?,?,?)
                """,
                (company, industry, int(consent), email, datetime.datetime.now())
            )
            conn.commit()
            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO assessments (user_id, total_score, risk_level, completed_at)
                VALUES (?,?,?,?)
                """,
                (user_id, total, risk_label, datetime.datetime.now())
            )
            conn.commit()
            assessment_id = cursor.lastrowid

            for q in questions:
                cursor.execute(
                    """
                    INSERT INTO responses (assessment_id, question_text, answer_value)
                    VALUES (?,?,?)
                    """,
                    (assessment_id, q["question"], st.session_state.responses.get(q["id"], 0))
                )
            conn.commit()

            # Save to JSON history (report path will be updated after AI advice loads)
            save_risk_score(
                st.session_state["username"],
                company,
                industry,
                total,
                categories,
                email,
                ""
            )

            st.session_state.results_saved = True

        # -------------------------
        # DISPLAY RESULTS
        # -------------------------
        st.subheader("Risk Score")
        st.write(round(total, 2))
        st.write(f"Risk Level: **{risk_label}**")

        # -------------------------
        # RISK GAUGE CHART
        # -------------------------

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(total, 2),
            title={"text": "Risk Score", "font": {"size": 20}},
            gauge={
                "axis": {
                    "range": [0, 200],
                    "tickwidth": 1,
                    "tickcolor": "gray",
                    "tickvals": [0, 50, 100, 150, 200],
                    "ticktext": ["0", "50", "100", "150", "200"]
                },
                "bar": {"color": "#6c64ff"},
                "steps": [
                    {"range": [0, 50],    "color": "#198754"},  # Green - Low
                    {"range": [50, 100],  "color": "#ffc107"},  # Yellow - Moderate
                    {"range": [100, 200], "color": "#dc3545"},  # Red - High
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": round(total, 2)
                }
            }
        ))

        fig_gauge.update_layout(
            height=400,
            margin={"t": 60, "b": 0, "l": 30, "r": 30},
            font={"color": "gray"}
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

        # Risk score reference table
        st.markdown("""
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <div style="flex: 1; padding: 12px; border-radius: 10px; background-color: #198754; color: white; text-align: center;">
                    <b>Low Risk</b><br>0 – 49
                </div>
                <div style="flex: 1; padding: 12px; border-radius: 10px; background-color: #ffc107; color: black; text-align: center;">
                    <b>Moderate Risk</b><br>50 – 99
                </div>
                <div style="flex: 1; padding: 12px; border-radius: 10px; background-color: #dc3545; color: white; text-align: center;">
                    <b>High Risk</b><br>100+
                </div>
            </div>
        """, unsafe_allow_html=True)

        # -------------------------
        # CATEGORY BREAKDOWN
        # -------------------------
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Category Breakdown")

        category_colors = {
            "Identify":  {"bg": "#0d6efd", "text": "white"},
            "Protect":   {"bg": "#6610f2", "text": "white"},
            "Detect":    {"bg": "#0dcaf0", "text": "black"},
            "Respond":   {"bg": "#ffc107", "text": "black"},
            "Recover":   {"bg": "#198754", "text": "white"},
        }

        cols = st.columns(len(categories))

        for col, (category, score) in zip(cols, categories.items()):
            color = category_colors.get(category, {"bg": "#6c757d", "text": "white"})
            col.markdown(f"""
                <div style="
                    padding: 15px;
                    border-radius: 10px;
                    background-color: {color['bg']};
                    color: {color['text']};
                    text-align: center;
                    box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
                    margin-bottom: 10px;
                ">
                    <b>{category}</b><br>
                    <span style="font-size: 22px; font-weight: 700;">{round(score, 2)}</span>
                </div>
            """, unsafe_allow_html=True)

        # -------------------------
        # AI ADVICE
        # -------------------------

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("AI-Generated Risk Advice")
        st.write("Powered by Groq's LLaMA 3.3")

        if "ai_advice" not in st.session_state:
            st.session_state.ai_advice = ""

        if not st.session_state.ai_advice:
            with st.spinner("Generating personalised security advice..."):
                try:
                    import requests

                    category_summary = "\n".join(
                        [f"- {cat}: {round(score, 2)}" for cat, score in categories.items()]
                    )

                    prompt = f"""
                    A company completed a cybersecurity risk assessment with the following results:

                    Industry: {industry}
                    Overall Risk Score: {round(total, 2)} ({risk_label} Risk)

                    Category Scores:
                    {category_summary}

                    Based on these results, provide clear and specific cybersecurity advice.
                    For each category with a high score, explain what the risk means and give 2-3 
                    actionable steps to improve it. Keep the tone professional but easy to understand.
                    Format your response with a heading for each category.
                    """

                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
                        },
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "max_tokens": 1000,
                            "messages": [{"role": "user", "content": prompt}]
                        }
                    )
                    data = response.json()
                    st.session_state.ai_advice = data["choices"][0]["message"]["content"]

                except Exception as e:
                    st.session_state.ai_advice = f"Could not generate advice: {e}, please check your API key."

        st.markdown(
            f"<div class='custom-card'>{st.session_state.ai_advice}</div>",
            unsafe_allow_html=True
        )
        
        # Generate report only after advice is ready
        if st.session_state.ai_advice and not st.session_state.report_path:
            try:
                report = generate_report(company, industry, total, categories, st.session_state.ai_advice)
                st.session_state.report_path = report

                # Update history with report path
                users = load_users()
                if st.session_state["username"] in users:
                    history = users[st.session_state["username"]]["history"]
                    if history:
                        history[-1]["report_path"] = report
                        save_users(users)

            except Exception as e:
                st.error(f"Report generation failed: {e}")

        # -------------------------
        # INDUSTRY BENCHMARK
        # -------------------------

        scores = get_industry_scores(industry)

        if scores:
            avg = sum(scores) / len(scores)
            percentile = sum(s < total for s in scores) / len(scores) * 100
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.subheader("CyberRisk Benchmark")
            st.write("Your Company's Score:", round(total, 2))
            st.write("CyberRisk Assessment Average:", round(avg, 2))
            st.write("Based on your results, your company is safer than", round(percentile, 1), "% of companies that have taken this assessment in the same industry.")

        # -------------------------
        # DOWNLOAD REPORT
        # -------------------------

        st.markdown("<br>", unsafe_allow_html=True)
        report_path = st.session_state.get("report_path", "")

        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as file:
                st.download_button(
                    "Download Security Report",
                    file.read(),
                    file_name=os.path.basename(report_path),
                    mime="application/pdf"
                )
        else:
            st.warning("Report not available. Please complete the assessment again.")
            
# -------------------------
# FOOTER
# -------------------------

st.markdown(
"""
<div class='footer'>
Disclaimer: This tool provides educational cybersecurity guidance based on
public frameworks such as NIST and CIS. Results should not replace
professional cybersecurity consultation.
</div>
""",
unsafe_allow_html=True
)
