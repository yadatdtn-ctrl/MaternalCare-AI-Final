import streamlit as st
import pickle
import numpy as np
from datetime import date, timedelta

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MaternalCare AI",
    page_icon="🤰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #fdf6ff; }

    /* Header banner */
    .main-header {
        background: linear-gradient(135deg, #6C3483, #A569BD);
        padding: 28px 24px 20px 24px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 28px;
        color: white;
    }
    .main-header h1 { margin: 0; font-size: 2.2rem; letter-spacing: 1px; }
    .main-header p  { margin: 6px 0 0; font-size: 1rem; opacity: 0.88; }

    /* Result boxes */
    .result-high {
        background: #fdecea; border-left: 6px solid #e74c3c;
        padding: 18px 20px; border-radius: 10px; margin-top: 14px;
    }
    .result-mid {
        background: #fef9ec; border-left: 6px solid #f39c12;
        padding: 18px 20px; border-radius: 10px; margin-top: 14px;
    }
    .result-low {
        background: #eafaf1; border-left: 6px solid #2ecc71;
        padding: 18px 20px; border-radius: 10px; margin-top: 14px;
    }
    .result-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 6px; }

    /* Info cards */
    .info-card {
        background: white; border-radius: 12px;
        padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-top: 10px;
    }

    /* Section divider */
    .section-title {
        font-size: 1.15rem; font-weight: 700;
        color: #6C3483; margin-bottom: 4px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #f3e8ff; }
</style>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    return model, le

try:
    model, le = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤰 MaternalCare AI</h1>
    <p>Maternal Health Risk Prediction · BMI Calculator · Expected Delivery Date</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/pregnant.png", width=80)
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "Choose a module:",
    ["🔬 Risk Prediction", "⚖️ BMI Calculator", "📅 Delivery Date"],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
**About MaternalCare AI**

A web-based system that combines machine learning with essential pregnancy health tools.

- **Risk Prediction** — Random Forest ML model
- **BMI** — Standard WHO formula
- **EDD** — Naegele's Rule

*MSE Project · Ramya · Yada · Celestine*
""")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — RISK PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
if page == "🔬 Risk Prediction":

    st.markdown('<p class="section-title">🔬 Maternal Health Risk Prediction</p>', unsafe_allow_html=True)
    st.caption("Enter your health measurements below. The AI model will predict your risk level.")

    if not model_loaded:
        st.error(
            "⚠️ Model files not found. Please run your notebook first to generate "
            "`rf_model.pkl` and `label_encoder.pkl`, then place them in the same folder as `app.py`."
        )
        st.stop()

    with st.form("risk_form"):
        st.markdown("#### Patient Health Inputs")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age (years)", min_value=10, max_value=70, value=25,
                help="Age of the patient in years."
            )
            systolic_bp = st.number_input(
                "Systolic Blood Pressure (mmHg)", min_value=70, max_value=180, value=120,
                help="Upper BP value. Normal range: 90–120 mmHg."
            )
            diastolic_bp = st.number_input(
                "Diastolic Blood Pressure (mmHg)", min_value=40, max_value=120, value=80,
                help="Lower BP value. Normal range: 60–80 mmHg."
            )

        with col2:
            bs = st.number_input(
                "Blood Sugar (mmol/L)", min_value=3.0, max_value=20.0,
                value=7.0, step=0.1,
                help="Blood glucose level in mmol/L."
            )
            body_temp = st.number_input(
                "Body Temperature (°F)", min_value=97.0, max_value=104.0,
                value=98.0, step=0.1,
                help="Normal body temperature: 97–99°F."
            )
            heart_rate = st.number_input(
                "Heart Rate (bpm)", min_value=40, max_value=100, value=76,
                help="Resting heart rate in beats per minute."
            )

        submitted = st.form_submit_button("🔍 Predict Risk Level", use_container_width=True)

    if submitted:
        input_data = np.array([[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]])
        prediction_encoded = model.predict(input_data)[0]
        prediction_label   = le.inverse_transform([prediction_encoded])[0]
        probabilities      = model.predict_proba(input_data)[0]

        # ── Result display ──────────────────────────────────────────────────
        if prediction_label == "high risk":
            css_class = "result-high"
            emoji = "🔴"
            advice = ("Your readings indicate <b>High Risk</b>. Please consult a doctor or "
                      "visit a maternal health clinic as soon as possible.")
        elif prediction_label == "mid risk":
            css_class = "result-mid"
            emoji = "🟡"
            advice = ("Your readings indicate <b>Mid Risk</b>. Monitor your health closely "
                      "and schedule a check-up with your healthcare provider.")
        else:
            css_class = "result-low"
            emoji = "🟢"
            advice = ("Your readings indicate <b>Low Risk</b>. Keep maintaining healthy habits "
                      "and continue regular prenatal check-ups.")

        st.markdown(f"""
        <div class="{css_class}">
            <div class="result-title">{emoji} Predicted Risk Level: {prediction_label.title()}</div>
            <p style="margin:0">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Confidence bar ──────────────────────────────────────────────────
        st.markdown("#### Model Confidence")
        class_order = ["high risk", "low risk", "mid risk"]  # alphabetical = LabelEncoder order
        for cls, prob in zip(le.classes_, probabilities):
            st.markdown(f"**{cls.title()}**")
            st.progress(float(prob), text=f"{prob*100:.1f}%")

        # ── Input summary ───────────────────────────────────────────────────
        with st.expander("📋 View Input Summary"):
            st.markdown(f"""
            | Parameter | Value | Normal Range |
            |---|---|---|
            | Age | {age} yrs | — |
            | Systolic BP | {systolic_bp} mmHg | 90–120 |
            | Diastolic BP | {diastolic_bp} mmHg | 60–80 |
            | Blood Sugar | {bs} mmol/L | 4.0–7.0 |
            | Body Temp | {body_temp} °F | 97–99 |
            | Heart Rate | {heart_rate} bpm | 60–90 |
            """)

        st.info("⚠️ This tool is for informational purposes only and does not replace professional medical advice.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — BMI CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚖️ BMI Calculator":

    st.markdown('<p class="section-title">⚖️ BMI Calculator</p>', unsafe_allow_html=True)
    st.caption("Calculate your Body Mass Index using the standard WHO formula.")

    with st.form("bmi_form"):
        st.markdown("#### Enter Your Measurements")
        col1, col2 = st.columns(2)

        with col1:
            weight = st.number_input(
                "Weight (kg)", min_value=30.0, max_value=200.0,
                value=60.0, step=0.5,
                help="Your current body weight in kilograms."
            )
        with col2:
            height_cm = st.number_input(
                "Height (cm)", min_value=100.0, max_value=220.0,
                value=160.0, step=0.5,
                help="Your height in centimetres."
            )

        submitted_bmi = st.form_submit_button("⚖️ Calculate BMI", use_container_width=True)

    if submitted_bmi:
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        # ── Category ────────────────────────────────────────────────────────
        if bmi < 18.5:
            category  = "Underweight"
            css_class = "result-mid"
            emoji     = "🟡"
            advice    = ("Your BMI is below the normal range. During pregnancy, being underweight "
                         "may increase the risk of low birth weight. Consider consulting a dietitian.")
        elif bmi < 25.0:
            category  = "Normal Weight"
            css_class = "result-low"
            emoji     = "🟢"
            advice    = ("Your BMI is within the healthy range. Maintain a balanced diet and "
                         "regular light exercise throughout your pregnancy.")
        elif bmi < 30.0:
            category  = "Overweight"
            css_class = "result-mid"
            emoji     = "🟡"
            advice    = ("Your BMI indicates overweight. During pregnancy, this may increase the "
                         "risk of gestational diabetes and hypertension. Speak to your doctor.")
        else:
            category  = "Obese"
            css_class = "result-high"
            emoji     = "🔴"
            advice    = ("Your BMI indicates obesity. Please consult your healthcare provider for "
                         "personalised guidance during your pregnancy.")

        st.markdown(f"""
        <div class="{css_class}">
            <div class="result-title">{emoji} BMI: {bmi:.2f} — {category}</div>
            <p style="margin:4px 0 0">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── BMI scale visual ────────────────────────────────────────────────
        st.markdown("#### BMI Categories")
        bmi_data = {
            "Underweight (< 18.5)":    "#3498db",
            "Normal (18.5 – 24.9)":    "#2ecc71",
            "Overweight (25.0 – 29.9)":"#f39c12",
            "Obese (≥ 30.0)":          "#e74c3c",
        }
        for label, colour in bmi_data.items():
            marker = " ◀ Your BMI" if label.split()[0].lower() == category.split()[0].lower() else ""
            st.markdown(
                f'<div style="background:{colour};color:white;padding:7px 14px;'
                f'border-radius:6px;margin:3px 0;font-weight:600">'
                f'{label}{marker}</div>',
                unsafe_allow_html=True
            )

        # ── Formula ─────────────────────────────────────────────────────────
        with st.expander("📐 Show Calculation"):
            st.markdown(f"""
            **Formula:** BMI = Weight (kg) ÷ Height² (m²)

            **Your values:**
            - Weight = {weight} kg
            - Height = {height_cm} cm = {height_m:.3f} m
            - Height² = {height_m:.3f}² = {height_m**2:.4f} m²

            **BMI = {weight} ÷ {height_m**2:.4f} = {bmi:.2f}**
            """)

        st.info("⚠️ BMI is a general indicator and does not account for all individual health factors.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — EXPECTED DELIVERY DATE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Delivery Date":

    st.markdown('<p class="section-title">📅 Expected Delivery Date Calculator</p>', unsafe_allow_html=True)
    st.caption("Calculate your Expected Delivery Date (EDD) using Naegele's Rule.")

    with st.form("edd_form"):
        st.markdown("#### Enter Your Last Menstrual Period (LMP) Date")

        lmp = st.date_input(
            "Last Menstrual Period (LMP)",
            value=date.today() - timedelta(weeks=8),
            max_value=date.today(),
            help="The first day of your last menstrual period."
        )

        submitted_edd = st.form_submit_button("📅 Calculate Due Date", use_container_width=True)

    if submitted_edd:
        edd          = lmp + timedelta(days=280)
        today        = date.today()
        days_elapsed = (today - lmp).days
        weeks_preg   = days_elapsed // 7
        days_rem     = days_elapsed % 7
        days_to_edd  = (edd - today).days
        trimester    = (
            "First Trimester (Weeks 1–12)"   if weeks_preg <= 12 else
            "Second Trimester (Weeks 13–26)" if weeks_preg <= 26 else
            "Third Trimester (Weeks 27–40)"
        )

        if days_to_edd < 0:
            css_class = "result-mid"
            edd_note  = f"Your EDD was {abs(days_to_edd)} day(s) ago. Please consult your doctor."
        elif days_to_edd == 0:
            css_class = "result-high"
            edd_note  = "Your expected delivery date is today! Please be in touch with your healthcare provider."
        else:
            css_class = "result-low"
            edd_note  = f"{days_to_edd} day(s) remaining until your expected delivery date."

        st.markdown(f"""
        <div class="{css_class}">
            <div class="result-title">🍼 Expected Delivery Date: {edd.strftime("%d %B %Y")}</div>
            <p style="margin:4px 0 0">{edd_note}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Pregnancy info cards ────────────────────────────────────────────
        st.markdown("#### Pregnancy Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Weeks Pregnant",  f"{weeks_preg}w {days_rem}d")
        c2.metric("Due Date",        edd.strftime("%d %b %Y"))
        c3.metric("Days Remaining",  max(0, days_to_edd))

        st.markdown(f"""
        <div class="info-card">
            <b>📌 Current Stage:</b> {trimester}<br><br>
            <b>📆 LMP Date:</b> {lmp.strftime("%d %B %Y")}<br>
            <b>📆 EDD Date:</b> {edd.strftime("%d %B %Y")}<br>
        </div>
        """, unsafe_allow_html=True)

        # ── Trimester guide ─────────────────────────────────────────────────
        st.markdown("#### Trimester Guide")
        trimesters = [
            ("🌱 First Trimester",  "Weeks 1–12",  "#d6eaf8", "Baby's organs begin forming. Morning sickness is common."),
            ("🌸 Second Trimester", "Weeks 13–26", "#d5f5e3", "Baby starts moving. Energy levels improve."),
            ("🌟 Third Trimester",  "Weeks 27–40", "#fef9e7", "Baby grows rapidly. Prepare for delivery."),
        ]
        for title, weeks, bg, desc in trimesters:
            current = "✅ " if weeks.split()[1].split("–")[0] <= str(weeks_preg) <= weeks.split("–")[1].replace("Weeks ","").split()[0] else ""
            st.markdown(
                f'<div style="background:{bg};padding:12px 16px;border-radius:8px;margin:4px 0">'
                f'<b>{current}{title}</b> <span style="color:#555">({weeks})</span><br>'
                f'<span style="font-size:0.9rem">{desc}</span></div>',
                unsafe_allow_html=True
            )

        # ── Formula ─────────────────────────────────────────────────────────
        with st.expander("📐 Show Calculation (Naegele's Rule)"):
            st.markdown(f"""
            **Naegele's Rule:** EDD = LMP + 280 days (40 weeks)

            - LMP = {lmp.strftime("%d %B %Y")}
            - EDD = {lmp.strftime("%d %B %Y")} + 280 days = **{edd.strftime("%d %B %Y")}**
            - Days elapsed since LMP = {days_elapsed} days = {weeks_preg} weeks and {days_rem} days
            """)

        st.info("⚠️ EDD is an estimate. Only about 5% of babies are born on their exact due date. Always consult your doctor.")
