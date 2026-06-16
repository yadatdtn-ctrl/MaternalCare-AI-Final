# Main Streamlit app for MaternalCare AI.
# Provides three tabs: BMI Calculator, Delivery Date, and Risk Prediction.

from datetime import date

import streamlit as st

from bmi_module import calculate_bmi, classify_bmi
from edd_module import calculate_edd, calculate_weeks
from risk_module import predict_maternal_risk

st.title("Maternalcare AI")
st.write("A smart health assistant for pregnant women")
st.divider()

tab1, tab2, tab3 = st.tabs(["BMI Calculator", "Delivery Date", "Risk Prediction"])

# --- Tab 1: BMI Calculator ---
with tab1:
    st.header("BMI Calculator")
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
    height = st.number_input("Height (cm)", min_value=1.0, value=165.0)

    if st.button("Calculate BMI"):
        height_m = height / 100
        bmi = calculate_bmi(weight, height_m)
        category = classify_bmi(bmi)
        st.metric("Your BMI", bmi)
        st.success(f"Category: {category}")

# --- Tab 2: Delivery Date ---
with tab2:
    st.header("Delivery Date")
    lmp = st.date_input("Last Menstrual Period (LMP)", value=date(2025, 9, 1))

    if st.button("Calculate Delivery Date"):
        edd = calculate_edd(lmp)
        weeks = calculate_weeks(lmp)
        st.metric("Expected Delivery Date", edd.strftime("%d %B %Y"))
        st.metric("Weeks Pregnant", f"Week {weeks}")

# --- Tab 3: Risk Prediction ---
with tab3:
    st.header("Risk Prediction")
    st.write("Enter health measurements to predict maternal risk level.")

    age = st.number_input(
        "Age",
        min_value=1,
        value=25,
        help="Patient age in years.",
    )
    systolic_bp = st.number_input(
        "Systolic BP (mmHg)",
        min_value=1,
        value=120,
        help="Top blood pressure number (when the heart beats). Normal is around 120 or below.",
    )
    diastolic_bp = st.number_input(
        "Diastolic BP (mmHg)",
        min_value=1,
        value=80,
        help="Bottom blood pressure number (when the heart rests). Normal is around 80 or below.",
    )
    bs = st.number_input(
        "Blood Sugar (BS)",
        min_value=1.0,
        value=7.0,
        help="Blood sugar level (mmol/L in this dataset). Values around 6–7 are typical.",
    )
    body_temp = st.number_input(
        "Body Temperature (°F)",
        min_value=90.0,
        value=98.0,
        help="Body temperature in Fahrenheit. Normal is around 98.6°F.",
    )
    heart_rate = st.number_input(
        "Heart Rate (bpm)",
        min_value=1,
        value=75,
        help="Heartbeats per minute (bpm). Normal resting rate is about 60–100 bpm.",
    )

    if st.button("Predict Risk"):
        risk = predict_maternal_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate)
        st.metric("Predicted Risk Level", risk)

        if risk == "low risk":
            st.success("Result: low risk")
            st.info("Your health indicators look good. Keep up regular check-ups.")
        elif risk == "mid risk":
            st.warning("Result: mid risk")
            st.info("Some indicators need attention. Please consult your doctor soon.")
        elif risk == "high risk":
            st.error("Result: high risk")
            st.info("Please consult your doctor immediately.")
        else:
            st.error(
                f"Unexpected prediction: {risk!r}. "
                "Expected 'low risk', 'mid risk', or 'high risk'."
            )
