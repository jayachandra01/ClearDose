# app.py

import streamlit as st
from utils import extract_text_from_pdf
from summarizer import simplify_text
from med_explainer import get_medication_info

st.set_page_config(page_title="ClearDose", layout="wide")
st.title("💊 ClearDose – Understand Your Prescription")

# File upload or text input
uploaded_file = st.file_uploader("Upload your medical report or prescription (PDF)", type=["pdf"])
raw_text = st.text_area("Or paste the prescription text here")

if st.button("Process"):
    with st.spinner("Extracting and summarizing..."):
        # Step 1: Extract text
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = raw_text
        
        if not text.strip():
            st.warning("Please upload a file or enter some text.")
        else:
            # Step 2: Summarize text
            summary = simplify_text(text)

            # Step 3: Get medication explanations
            med_info = get_medication_info(text)

            # Step 4: Display output
            st.subheader("📝 Simplified Summary")
            st.write(summary)

            st.subheader("💊 Medication Explanations")
            if med_info:
                for med, info in med_info.items():
                    st.markdown(f"**{med.capitalize()}**")
                    st.markdown(info or "⚠️ No information found.")
            else:
                st.info("No medications detected in the text.")
