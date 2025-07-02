
import streamlit as st
from transformers import pipeline
import json

# Load test ranges
with open("test_ranges.json", "r") as f:
    TEST_RANGES = json.load(f)

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2", device_map="auto")

med_bot = load_model()

def explain_medication(drug_name, tone="simple"):
    prompt = f"Explain the medicine '{drug_name}' in {tone} language. Include what it is, what it treats, how to take it, common side effects, and important warnings. End with: This is not medical advice. Always consult a doctor."
    result = med_bot(prompt, max_new_tokens=300)[0]["generated_text"]
    return result

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

        prompt = f"Explain the lab test '{test_name}' in layman terms. The result is {value} {unit}, which is {status}. Normal range is {normal_low} to {normal_high} {unit}. Include what it measures, what this result means, and advice. End with a disclaimer."
    else:
        prompt = f"Explain the lab test result: {test_name}: {test_value_str}. What does this mean in simple terms? Include possible implications and a disclaimer."

    result = med_bot(prompt, max_new_tokens=300)[0]["generated_text"]
    return result

st.set_page_config(page_title="MedExplain.ai (Hugging Face)", page_icon="🩺")
st.title("🩺 MedExplain.ai")
st.markdown("Explain medications and lab test results in plain language — powered by Hugging Face 🤗")

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
