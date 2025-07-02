
import streamlit as st
import openai
import json

# Load normal ranges for lab tests
with open("test_ranges.json", "r") as f:
    TEST_RANGES = json.load(f)

# Set your OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to generate medication explanation
def explain_medication(drug_name, tone="simple"):
    prompt = f"""
You are a helpful medical assistant. Explain the following drug in {tone} language.
Drug: {drug_name}
Explain:
1. What it is
2. What it treats
3. How to take it
4. Common side effects
5. Important warnings (if any)
End with: “This is not medical advice. Always consult a doctor.”
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message["content"]

# Function to generate lab test explanation
def explain_lab_test(test_name, test_value_str):
    try:
        value = float(test_value_str.replace("%", "").replace("mg/dL", "").strip())
    except:
        return "⚠️ Please enter a valid numerical value."

    if test_name in TEST_RANGES:
        test_info = TEST_RANGES[test_name]
        normal_low, normal_high = test_info["normal_range"]
        unit = test_info["unit"]
        url = test_info["source"]

        status = (
            "normal ✅" if normal_low <= value <= normal_high else
            "high 🔺" if value > normal_high else
            "low 🔻"
        )

        prompt = f"""
You are a medical assistant that explains lab test results in plain English.

Test: {test_name}
Result: {value} {unit} ({status})
Normal Range: {normal_low} - {normal_high} {unit}

Explain:
1. What this test measures
2. What this result might indicate
3. Any lifestyle or medical recommendations
End with: “This is not medical advice. Always consult a doctor.”

Source: {url}
        """
    else:
        prompt = f"""
The user entered a lab result: {test_name}: {test_value_str}.
Explain what this means in simple language. If the result seems high or low, mention what it might indicate and suggest consulting a doctor. End with a disclaimer.
        """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message["content"]

# Streamlit UI
st.set_page_config(page_title="MedExplain.ai", page_icon="🩺")
st.title("🩺 MedExplain.ai")
st.markdown("Explain medications and lab test results in plain language.")

tab1, tab2 = st.tabs(["💊 Medication Info", "🧪 Lab Test Result"])

with tab1:
    drug = st.text_input("Enter a medication name:")
    tone = st.radio("Choose explanation style:", ["simple", "formal"])
    if st.button("Explain Medication"):
        if drug:
            st.info("Generating explanation...")
            result = explain_medication(drug, tone)
            st.success(result)
        else:
            st.warning("Please enter a medication name.")

with tab2:
    test_input = st.text_input("Enter lab test (e.g. 'Hemoglobin A1C')")
    test_value = st.text_input("Enter value (e.g. '8.3%')")
    if st.button("Explain Lab Result"):
        if test_input and test_value:
            st.info("Analyzing result...")
            result = explain_lab_test(test_input, test_value)
            st.success(result)
        else:
            st.warning("Please fill in both fields.")
