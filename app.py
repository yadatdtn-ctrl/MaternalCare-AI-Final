# MaternalCare AI - Main Streamlit Application
# Redesigned with Warm Blossom design system and onboarding flow.

from datetime import date

import streamlit as st

from bmi_module import calculate_bmi, classify_bmi
from edd_module import calculate_edd, calculate_weeks, get_trimester, days_until_edd
from risk_module import predict_maternal_risk, get_model_accuracy

# -- Weekly pregnancy content dictionary --------------------------------------
WEEKLY_UPDATES = {
    1: {"size": "poppy seed", "highlight": "The fertilised egg has implanted. Your baby's neural tube is beginning to form.", "mama": "You may not feel any different yet. Take folic acid daily."},
    2: {"size": "sesame seed", "highlight": "Cell division is happening rapidly. The placenta is starting to develop.", "mama": "Rest as much as you need. Your body is working hard."},
    3: {"size": "lentil", "highlight": "Your baby's heart is beginning to beat. Tiny arm and leg buds are forming.", "mama": "Nausea may begin this week. Small frequent meals can help."},
    4: {"size": "blueberry", "highlight": "Brain and spinal cord are developing quickly. Tiny facial features are forming.", "mama": "Fatigue is very common now. Your body is building a whole new life."},
    5: {"size": "raspberry", "highlight": "Your baby's heart is now beating 100-160 times per minute.", "mama": "Morning sickness may peak this week. Ginger tea can help."},
    6: {"size": "grape", "highlight": "Fingers and toes are forming. Your baby can now move, though you cannot feel it yet.", "mama": "You may notice your clothes feeling slightly tighter."},
    7: {"size": "strawberry", "highlight": "Your baby can now hiccup! All major organs are developing.", "mama": "Your blood volume is increasing - stay well hydrated."},
    8: {"size": "lime", "highlight": "Tiny fingernails are forming. Your baby is now officially called a fetus.", "mama": "You may notice skin changes. This is normal and temporary."},
    9: {"size": "lemon", "highlight": "Your baby can now swallow and produce urine. Taste buds are forming.", "mama": "Your uterus is now the size of a grapefruit."},
    10: {"size": "apple", "highlight": "Your baby's bones are beginning to harden. She can now make facial expressions.", "mama": "Energy levels often improve around this week."},
    11: {"size": "avocado", "highlight": "Your baby can now hear sounds from outside the womb.", "mama": "Your bump may start becoming visible this week."},
    12: {"size": "banana", "highlight": "Your baby has developed all her major organs. Growth now accelerates.", "mama": "Many mothers start to feel much better after week 12."},
    13: {"size": "mango", "highlight": "Your baby's eyes are sensitive to light even though the eyelids are fused.", "mama": "Welcome to the second trimester - often the most comfortable period."},
    14: {"size": "large mango", "highlight": "Your baby's facial muscles are developed enough to make expressions.", "mama": "You may notice your hair and nails growing faster."},
    15: {"size": "bell pepper", "highlight": "Your baby is now practising breathing movements using amniotic fluid.", "mama": "Some mothers start feeling gentle flutters of movement this week."},
    16: {"size": "avocado", "highlight": "Your baby's skeleton is forming. She can now yawn and stretch.", "mama": "Your energy is likely at its highest point of the pregnancy."},
    17: {"size": "onion", "highlight": "Your baby's fingerprints are now fully formed - completely unique to her.", "mama": "You may start to feel baby movements called quickening."},
    18: {"size": "sweet potato", "highlight": "Your baby can now hear your heartbeat and your voice clearly.", "mama": "Talk and sing to your baby - she recognises your voice already."},
    19: {"size": "mango", "highlight": "A protective coating called vernix is forming over your baby's skin.", "mama": "Back pain may begin as your centre of gravity shifts."},
    20: {"size": "banana", "highlight": "Halfway there! Your baby is now swallowing several times a day.", "mama": "Your 20-week anatomy scan is usually scheduled around now."},
    21: {"size": "carrot", "highlight": "Your baby's eyebrows and eyelashes are now fully developed.", "mama": "You may notice Braxton Hicks contractions - practice contractions that are normal."},
    22: {"size": "papaya", "highlight": "Your baby can now hear sounds from outside your body. She may respond to music.", "mama": "Your belly button may start to pop outward this week."},
    23: {"size": "large mango", "highlight": "Your baby is developing a sense of movement and can feel you dance.", "mama": "Leg cramps are common now. Stay hydrated and stretch before bed."},
    24: {"size": "corn cob", "highlight": "Your baby now has a regular sleep and wake cycle.", "mama": "If born now, your baby has a chance of survival with specialist care. A big milestone."},
    25: {"size": "cauliflower", "highlight": "Your baby's nostrils are opening and she is practising breathing.", "mama": "Heartburn may increase as your uterus pushes upward."},
    26: {"size": "lettuce", "highlight": "Your baby's eyes are opening for the first time and she can blink.", "mama": "You are in the final stretch of the second trimester."},
    27: {"size": "cabbage", "highlight": "Your baby can now recognise your voice and may respond to it.", "mama": "Welcome to the third trimester - the final chapter of your journey."},
    28: {"size": "large eggplant", "highlight": "Your baby's brain is developing rapidly. She can now dream.", "mama": "Kick counting begins now. You should feel at least 10 kicks in 2 hours."},
    29: {"size": "butternut squash", "highlight": "Your baby is gaining weight rapidly to prepare for life outside the womb.", "mama": "Shortness of breath is common as your uterus presses on your diaphragm."},
    30: {"size": "large cabbage", "highlight": "Your baby is now storing iron, calcium and phosphorus in her bones.", "mama": "Sleep may become more difficult. A pillow between your knees can help."},
    31: {"size": "coconut", "highlight": "All five senses are now fully developed.", "mama": "Frequent urination returns as the baby drops lower into your pelvis."},
    32: {"size": "jicama", "highlight": "Your baby is practising all the skills she will need at birth.", "mama": "Your hospital bag should be packed and ready from this week."},
    33: {"size": "pineapple", "highlight": "Your baby is now detecting light and dark through your belly.", "mama": "Braxton Hicks contractions may become more frequent and noticeable."},
    34: {"size": "cantaloupe", "highlight": "Your baby's lungs are almost fully mature.", "mama": "You may feel increased pressure in your pelvis as the baby descends."},
    35: {"size": "honeydew melon", "highlight": "Your baby's kidneys are fully developed and her liver can process waste.", "mama": "Rest as much as possible. Your body is preparing for labour."},
    36: {"size": "large romaine lettuce", "highlight": "Your baby is considered early term. Most organs are fully ready.", "mama": "You may feel the baby drop lower - this is called lightening."},
    37: {"size": "winter melon", "highlight": "Your baby is full term. She is ready to be born at any time.", "mama": "Watch for signs of labour: regular contractions, water breaking, bloody show."},
    38: {"size": "leek", "highlight": "Your baby is shedding the vernix coating and fine body hair.", "mama": "Stay close to home and keep your hospital bag by the door."},
    39: {"size": "mini watermelon", "highlight": "Your baby's brain and lungs continue developing right up until birth.", "mama": "Any day now. Trust your body - it knows what to do."},
    40: {"size": "small pumpkin", "highlight": "Your baby is fully ready. Her skull bones are still flexible for birth.", "mama": "You made it to your due date. Every day is a gift now. You are amazing."},
}

# -- Page configuration --------------------------------------------------------
st.set_page_config(
    page_title="MaternalCare AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -- Global CSS - Warm Blossom design system -----------------------------------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #FDF6F0;
    }

    /* Hide default Streamlit header/footer chrome */
    #MainMenu, footer { visibility: hidden; }

    /* Primary buttons */
    .stButton > button {
        background-color: #C4956A;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #A97B52;
        color: #ffffff;
        border: none;
    }
    .stButton > button:active {
        background-color: #8F6540;
        color: #ffffff;
    }

    /* Active tab - terracotta bottom border */
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #C4956A !important;
        color: #C4956A !important;
        font-weight: 700;
    }

    /* st.metric value colour */
    [data-testid="stMetricValue"] {
        color: #C4956A !important;
        font-size: 1.4rem !important;
        font-weight: 700;
    }

    /* Card container feel */
    .card {
        background-color: #ffffff;
        border: 1px solid #E8C4A0;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        background-color: #D4A2C2;
        color: #ffffff;
        border-radius: 20px;
        padding: 0.2rem 0.9rem;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }

    /* Body text and subheader colour */
    h3 {
        color: #5C3D1E !important;
    }

    /* st.metric label colour */
    [data-testid="stMetricLabel"] {
        color: #5C3D1E !important;
        font-weight: 600;
    }

    /* Disclaimer / caption text */
    .disclaimer {
        color: #5C3D1E;
        font-size: 0.82rem;
        font-style: italic;
        margin-top: 0.5rem;
        opacity: 0.75;
    }

    /* Welcome screen centering */
    .welcome-center {
        text-align: center;
        margin: 0 auto;
        max-width: 520px;
        padding: 2rem 1rem;
    }

    /* Onboarding card */
    .onboarding-card {
        background-color: #ffffff;
        border: 1px solid #E8C4A0;
        border-radius: 16px;
        padding: 2rem 2.4rem;
        max-width: 520px;
        margin: 0 auto;
    }

    /* Force light theme on sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F5EBE0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #5C3D1E !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #C4956A !important;
        color: #ffffff !important;
    }

    /* Force light theme on all input fields */
    input[type="number"], input[type="text"] {
        background-color: #ffffff !important;
        color: #5C3D1E !important;
        border: 1px solid #E8C4A0 !important;
        border-radius: 8px !important;
    }

    /* Date input and selectbox */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #E8C4A0 !important;
        color: #5C3D1E !important;
    }

    /* Selectbox dropdown text */
    div[data-baseweb="select"] span {
        color: #5C3D1E !important;
    }

    /* Tab bar background */
    div[data-testid="stTabs"] {
        background-color: transparent !important;
    }

    /* Fix tab label text visibility */
    button[data-baseweb="tab"] p {
        color: #8B6045 !important;
        font-size: 14px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #C4956A !important;
        font-weight: 600 !important;
    }

    /* Progress bar unfilled track - soft warm background */
    div[data-testid="stProgress"] > div > div {
        background-color: #EDD9C8 !important;
    }

    /* Progress bar color - filled portion (covers all Streamlit versions) */
    div[data-testid="stProgress"] > div > div > div,
    [data-testid="stProgressBar"] {
        background-color: #C4956A !important;
    }

    /* Fix home tab bullet points - the st.write() icons */
    p {
        color: #5C3D1E !important;
    }

    /* Metric value and label colors */
    div[data-testid="stMetric"] label {
        color: #8B6045 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #C4956A !important;
    }

    /* Overall app text color */
    .stApp p, .stApp li, .stApp span {
        color: #5C3D1E;
    }

    /* Caption text */
    div[data-testid="stCaptionContainer"] p {
        color: #8B6045 !important;
    }

    /* Fix dark +/- stepper buttons on number inputs */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #E8C4A0 !important;
        color: #5C3D1E !important;
        border: none !important;
    }
    /* Hide Streamlit top header bar */
    header[data-testid="stHeader"] {
        background-color: #FDF6F0 !important;
    }

    /* Onboarding form submit button (st.form_submit_button) */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #C4956A !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #A97B52 !important;
        color: #ffffff !important;
    }

    /* Force light theme on ALL Streamlit popups and overlays */
    div[role="listbox"],
    div[role="option"],
    ul[role="listbox"] {
        background-color: #FDF6F0 !important;
        color: #4A3728 !important;
    }

    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
        background-color: #EDD9C8 !important;
        color: #4A3728 !important;
    }

    /* Nuclear option - force ALL calendar children to light theme */
    div[data-baseweb="calendar"] *,
    div[data-baseweb="datepicker"] * {
        background-color: #FDF6F0 !important;
        color: #4A3728 !important;
        border-color: #EDD9C8 !important;
    }

    /* Re-apply selected date on top */
    div[data-baseweb="calendar"] [aria-selected="true"],
    div[data-baseweb="calendar"] [aria-selected="true"] * {
        background-color: #C4956A !important;
        color: #ffffff !important;
    }

    /* Re-apply hover on top */
    div[data-baseweb="calendar"] button:hover,
    div[data-baseweb="calendar"] button:hover * {
        background-color: #EDD9C8 !important;
        color: #4A3728 !important;
    }

    /* Disabled/empty cells */
    div[data-baseweb="calendar"] button:disabled *,
    div[data-baseweb="calendar"] button[disabled] * {
        background-color: #FDF6F0 !important;
        color: #C4956A !important;
        opacity: 0.3 !important;
    }

    /* Popover container */
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul {
        background-color: #FDF6F0 !important;
    }

    /* Empty placeholder cells in calendar grid - direct role targeting */
    div[role="gridcell"],
    div[role="gridcell"] * {
        background-color: #FDF6F0 !important;
    }

    /* First/last row empty cells */
    div[data-baseweb="calendar"] div[role="grid"] div:empty {
        background-color: #FDF6F0 !important;
    }

    /* Override any inline dark background on calendar grid rows */
    div[data-baseweb="calendar"] div[role="row"],
    div[data-baseweb="calendar"] div[role="row"] > div {
        background-color: #FDF6F0 !important;
    }
    /* Portal-level popover - targets month/year lists rendered outside the calendar div */
    body div[data-baseweb="popover"],
    body div[data-baseweb="popover"] *,
    body [data-baseweb="menu"],
    body [data-baseweb="menu"] * {
        background-color: #FDF6F0 !important;
        color: #4A3728 !important;
    }

    /* Selected item inside portal dropdown */
    body [data-baseweb="menu"] [aria-selected="true"],
    body [data-baseweb="menu"] li[aria-selected="true"] * {
        background-color: #C4956A !important;
        color: #ffffff !important;
    }

    /* Empty placeholder cells in calendar grid */
    div[data-baseweb="calendar"] div[role="grid"] > div,
    div[data-baseweb="calendar"] div[role="grid"] > div > div {
        background-color: #FDF6F0 !important;
    }

    /* Override browser autofill grey background on text inputs */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        -webkit-box-shadow: 0 0 0 30px #FFFFFF inset !important;
        -webkit-text-fill-color: #4A3728 !important;
        caret-color: #4A3728 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -- Helper: BMI progress value capped to [0, 1] for st.progress() -------------
def bmi_progress(bmi: float) -> float:
    """Map BMI onto a 0-1 scale anchored at 40 max for display."""
    return min(max(bmi / 40.0, 0.0), 1.0)


# ===============================================================================
# WELCOME / ONBOARDING SCREEN
# Shown once per session until the user submits the form.
# ===============================================================================
if "user_name" not in st.session_state:

    # Centre column layout for the onboarding card
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown(
            "<div style='text-align:center; margin-top:2rem;'>"
            "<span style='font-size:4rem;'>🌸</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='text-align:center; color:#C4956A; margin-bottom:0.2rem;'>"
            "Welcome to MaternalCare AI</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#5C3D1E; margin-bottom:1.8rem;'>"
            "Your personal health companion throughout your pregnancy</p>",
            unsafe_allow_html=True,
        )

        # Onboarding form
        with st.form("onboarding_form"):
            name_input = st.text_input("What is your name?", placeholder="e.g. Amara")

            lmp_input = st.date_input(
                "When was your last menstrual period (LMP)?",
                value=date(2025, 9, 1),
                min_value=date(2023, 1, 1),
                max_value=date.today(),
            )

            status_input = st.selectbox(
                "How are you using this app today?",
                options=[
                    "I am currently pregnant",
                    "I am planning a pregnancy",
                    "I am a healthcare student or researcher",
                ],
            )

            submitted = st.form_submit_button("Begin my journey ->", use_container_width=True)

            if submitted:
                if not name_input.strip():
                    st.warning("Please enter your name to continue.")
                else:
                    st.session_state["user_name"] = name_input.strip()
                    st.session_state["lmp_date"] = lmp_input
                    st.session_state["user_status"] = status_input
                    st.rerun()

        st.markdown(
            "<p class='disclaimer' style='text-align:center; margin-top:1rem;'>"
            "We do not store any of your information. "
            "Everything stays private on your device.</p>",
            unsafe_allow_html=True,
        )

    # Stop rendering the rest of the app until the form is submitted
    st.stop()


# ===============================================================================
# MAIN APP - shown after onboarding is complete
# ===============================================================================

# -- Sidebar: "Start over" reset button ----------------------------------------
with st.sidebar:
    st.markdown("### MaternalCare AI 🌸")
    st.markdown(f"Signed in as **{st.session_state['user_name']}**")
    st.divider()
    if st.button("Start over"):
        for key in ["user_name", "lmp_date", "user_status"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# -- Tab layout -----------------------------------------------------------------
tab_home, tab_pregnancy, tab_risk = st.tabs(
    ["🏠 Home", "📊 My Pregnancy", "🩺 Risk Assessment"]
)


# ===============================================================================
# TAB 1 - Home
# ===============================================================================
with tab_home:

    # Personalised greeting and status badge
    st.markdown(
        f"<div class='status-badge'>{st.session_state['user_status']}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h2 style='color:#C4956A; margin-bottom:0.1rem;'>"
        f"Welcome back, {st.session_state['user_name']} 🌸</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#5C3D1E; margin-bottom:1.5rem;'>"
        "Your personal health companion throughout your pregnancy journey</p>",
        unsafe_allow_html=True,
    )

    # What the app does
    st.write("📏 **BMI tracker** - monitor your weight and height throughout pregnancy")
    st.write("📅 **Due date calculator** - know exactly how many weeks along you are")
    st.write("🩺 **AI risk assessment** - check key health indicators with one click")

    st.divider()

    # Pregnancy progress bar - uses LMP stored during onboarding
    st.subheader("Your pregnancy progress")
    lmp_home = st.session_state["lmp_date"]
    weeks_home = calculate_weeks(lmp_home)
    weeks_capped = min(max(weeks_home, 0), 40)
    progress_fraction = weeks_capped / 40

    st.progress(progress_fraction)
    st.caption(f"Week {weeks_capped} of 40 - based on your LMP ({lmp_home.strftime('%d %B %Y')})")

    # Trimester badge and days remaining
    trimester_name, trimester_range = get_trimester(weeks_capped)
    edd_home = calculate_edd(lmp_home)
    days_left = days_until_edd(edd_home)

    col_trim, col_days = st.columns(2)
    with col_trim:
        st.markdown(
            f"<div style='background:#D4A2C2;color:#fff;border-radius:20px;"
            f"padding:0.3rem 1rem;display:inline-block;font-size:13px;"
            f"font-weight:600;margin-top:6px;'>"
            f"{trimester_name} - {trimester_range}</div>",
            unsafe_allow_html=True,
        )
    with col_days:
        st.metric("Days until due date", days_left)

    st.divider()

    # Baby this week card
    st.subheader("Your baby this week")
    weeks_display = min(max(weeks_capped, 1), 40)
    update = WEEKLY_UPDATES.get(weeks_display, WEEKLY_UPDATES[20])

    col_baby, col_mama = st.columns(2)
    with col_baby:
        st.markdown(
            f"<div style='background:#FDF6F0;border:1px solid #E8C4A0;"
            f"border-radius:12px;padding:1rem 1.2rem;height:100%;'>"
            f"<div style='font-size:11px;color:#8B6045;font-weight:600;"
            f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
            f"Week {weeks_display} - Baby</div>"
            f"<div style='font-size:16px;font-weight:600;color:#C4956A;margin-bottom:6px;'>"
            f"About the size of a {update['size']}</div>"
            f"<div style='font-size:14px;color:#5C3D1E;line-height:1.6;'>"
            f"{update['highlight']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_mama:
        st.markdown(
            f"<div style='background:#F0F6F3;border:1px solid #B8D4C8;"
            f"border-radius:12px;padding:1rem 1.2rem;height:100%;'>"
            f"<div style='font-size:11px;color:#3A6B55;font-weight:600;"
            f"text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>"
            f"For you this week</div>"
            f"<br>"
            f"<div style='font-size:14px;color:#2D5245;line-height:1.6;'>"
            f"{update['mama']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Summary metric cards
    st.subheader("Your health snapshot")
    col_bmi, col_edd, col_risk = st.columns(3)

    with col_bmi:
        bmi_val = st.session_state.get("bmi_result")
        bmi_cat = st.session_state.get("bmi_category")
        st.metric(
            label="BMI",
            value=str(bmi_val) if bmi_val else "-",
            delta=bmi_cat if bmi_cat else "Not yet calculated",
        )

    with col_edd:
        edd_val = st.session_state.get("edd_result")
        st.metric(
            label="Due date",
            value=edd_val if edd_val else "-",
            delta="Not yet calculated" if not edd_val else f"Week {weeks_home} of 40",
        )

    with col_risk:
        risk_val = st.session_state.get("risk_result")
        st.metric(
            label="Risk level",
            value=risk_val.title() if risk_val else "-",
            delta="Not yet assessed" if not risk_val else "See Risk Assessment tab",
        )

# Warning signs section
    st.divider()
    st.subheader("Warning signs - when to contact your doctor")
    st.markdown(
        "<p style='color:#8B6045;font-size:13px;margin-bottom:1rem;'>"
        "These symptoms need prompt medical attention. "
        "When in doubt, always call your healthcare provider.</p>",
        unsafe_allow_html=True,
    )

    warning_signs = [
        {"color": "#C4607A", "bg": "#FDF0F2",
         "symptom": "Severe headache, vision changes, or sudden face or hand swelling",
         "action": "Call your doctor immediately - may indicate preeclampsia."},
        {"color": "#C4607A", "bg": "#FDF0F2",
         "symptom": "Heavy vaginal bleeding at any stage",
         "action": "Go to the emergency room immediately."},
        {"color": "#C4607A", "bg": "#FDF0F2",
         "symptom": "Fewer than 10 kicks in 2 hours after week 28",
         "action": "Contact your midwife or doctor the same day."},
        {"color": "#C4956A", "bg": "#FDF6EE",
         "symptom": "Regular contractions before week 37",
         "action": "Call your doctor - may be preterm labour."},
        {"color": "#C4956A", "bg": "#FDF6EE",
         "symptom": "Burning or pain when urinating",
         "action": "Contact your doctor - likely a UTI that needs treatment."},
        {"color": "#7BAD9B", "bg": "#F0F6F3",
         "symptom": "Mild swelling in ankles and feet",
         "action": "Common and normal. Rest with feet elevated. Mention at next visit."},
        {"color": "#7BAD9B", "bg": "#F0F6F3",
         "symptom": "Braxton Hicks contractions (irregular, no pattern)",
         "action": "Normal practice contractions. If they become regular, time them."},
    ]

    for sign in warning_signs:
        st.markdown(
            f"<div style='background:{sign['bg']};border-left:3px solid {sign['color']};"
            f"border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:8px;'>"
            f"<div style='font-size:13px;font-weight:600;color:{sign['color']};"
            f"margin-bottom:2px;'>{sign['symptom']}</div>"
            f"<div style='font-size:12px;color:#5C3D1E;'>{sign['action']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p style='font-size:11px;color:#8B6045;font-style:italic;margin-top:8px;'>"
        "This list is for general guidance only and does not replace professional "
        "medical advice. Always follow your healthcare provider's instructions.</p>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        "<p class='disclaimer'>"
        "This app supports - but does not replace - professional medical advice.</p>",
        unsafe_allow_html=True,
    )


# ===============================================================================
# TAB 2 - My Pregnancy (BMI + EDD side by side)
# ===============================================================================
with tab_pregnancy:

    col_bmi_tab, col_edd_tab = st.columns(2)

    # -- Left column: BMI Calculator -------------------------------------------
    with col_bmi_tab:
        with st.container():
            st.subheader("BMI calculator")

            weight = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=65.0,
                step=0.1,
            )
            height_cm = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=250.0,
                value=165.0,
                step=0.1,
            )

            if st.button("Calculate BMI"):
                height_m = height_cm / 100
                bmi = calculate_bmi(weight, height_m)
                category = classify_bmi(bmi)

                # Persist results for the Home tab snapshot
                st.session_state["bmi_result"] = bmi
                st.session_state["bmi_category"] = category

                st.metric("Your BMI", bmi)

                # Category colour mapping
                cat_colours = {
                    "Underweight": "#E8A87C",
                    "Normal": "#7BAD9B",
                    "Overweight": "#C4607A",
                }
                colour = cat_colours.get(category, "#C4956A")
                st.markdown(
                    f"<div style='background:{colour}; color:#fff; border-radius:8px; "
                    f"padding:0.4rem 0.9rem; display:inline-block; font-weight:600; "
                    f"margin-bottom:0.8rem;'>{category}</div>",
                    unsafe_allow_html=True,
                )

                # Visual BMI range bar
                st.caption("BMI range indicator  (Underweight < 18.5 | Normal 18.5-24.9 | Overweight > 25)")
                st.progress(bmi_progress(bmi))

                if category == "Underweight":
                    st.info("Your BMI suggests you may need extra nutritional support. Please discuss this with your midwife or doctor.")
                elif category == "Normal":
                    st.success("Your BMI is within a healthy range. Keep nourishing yourself well.")
                else:
                    st.warning("Your BMI is above the normal range. Please consult your doctor for personalised guidance.")

    # -- Right column: Expected Delivery Date ----------------------------------
    with col_edd_tab:
        with st.container():
            st.subheader("Expected delivery date")

            # Pre-fill with the LMP entered at onboarding
            lmp_default = st.session_state.get("lmp_date", date(2025, 9, 1))
            lmp = st.date_input(
                "Last menstrual period (LMP)",
                value=lmp_default,
                min_value=date(2023, 1, 1),
                max_value=date.today(),
                key="edd_lmp_input",
            )

            if st.button("Calculate due date"):
                edd = calculate_edd(lmp)
                weeks = calculate_weeks(lmp)
                weeks_display = min(max(weeks, 0), 40)

                edd_str = edd.strftime("%d %B %Y")
                # Persist for Home tab snapshot
                st.session_state["edd_result"] = edd_str
                st.session_state["lmp_date"] = lmp  # update if user changed it

                st.metric("Expected delivery date", edd_str)
                st.metric("Weeks pregnant", f"Week {weeks_display} of 40")

                # Pregnancy progress bar
                st.caption("Pregnancy progress")
                progress_val = min(max(weeks_display / 40, 0.0), 1.0)
                st.progress(progress_val)

                if weeks_display < 13:
                    st.info("You are in the first trimester. Regular early check-ups are especially important now.")
                elif weeks_display < 27:
                    st.success("You are in the second trimester - many mothers feel their best during this stage!")
                elif weeks_display <= 40:
                    st.warning("You are in the third trimester. Make sure your birth plan is ready and your doctor is close by.")


# ===============================================================================
# TAB 3 - Risk Assessment (ML prediction)
# ===============================================================================
with tab_risk:

    st.subheader("AI risk assessment")
    st.write("Enter your latest health measurements below. All fields are required.")

    col_left, col_right = st.columns(2)

    # -- Left column inputs ----------------------------------------------------
    with col_left:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25,
            help="Your age in years.",
        )
        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=1,
            max_value=300,
            value=120,
            help="Top blood pressure number (when the heart beats). Normal is around 120 or below.",
        )
        diastolic_bp = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=1,
            max_value=200,
            value=80,
            help="Bottom blood pressure number (when the heart rests). Normal is around 80 or below.",
        )

    # -- Right column inputs ---------------------------------------------------
    with col_right:
        bs = st.number_input(
            "Blood sugar (mmol/L)",
            min_value=1.0,
            max_value=30.0,
            value=7.0,
            step=0.1,
            help="Blood sugar level (mmol/L in this dataset). Values around 6-7 are typical.",
        )
        body_temp = st.number_input(
            "Body temperature (degF)",
            min_value=90.0,
            max_value=110.0,
            value=98.0,
            step=0.1,
            help="Body temperature in Fahrenheit. Normal is around 98.6 F.",
        )
        heart_rate = st.number_input(
            "Heart rate (bpm)",
            min_value=1,
            max_value=250,
            value=75,
            help="Heartbeats per minute (bpm). Normal resting rate is about 60-100 bpm.",
        )

    st.write("")  # spacer

    # Predict button - full width for visibility
    if st.button("Check my risk level", use_container_width=True):
        risk = predict_maternal_risk(
            age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate
        )
        # Persist for Home tab snapshot
        st.session_state["risk_result"] = risk

        # Model accuracy - builds user trust
        accuracy = get_model_accuracy()
        st.caption(f"AI model accuracy: {accuracy}%")

        st.divider()

        if risk == "low risk":
            st.success(
                "Your health indicators look wonderful. "
                "Keep up your regular check-ups and stay well-hydrated."
            )
        elif risk == "mid risk":
            st.warning(
                "[!]  A few indicators need attention. "
                "We recommend scheduling a check-up with your doctor soon. "
                "You are doing great by staying informed."
            )
        elif risk == "high risk":
            st.error(
                "🩺  Some of your indicators need immediate attention. "
                "Please contact your healthcare provider today. "
                "You are not alone - help is available."
            )
        else:
            st.warning(
                f"Unexpected result: {risk!r}. "
                "Please consult your doctor for a proper assessment."
            )

    st.divider()
    st.markdown(
        "<p class='disclaimer'>"
        "This tool uses an AI model trained on anonymised health data. "
        "It does not replace a clinical diagnosis.</p>",
        unsafe_allow_html=True,
    )
