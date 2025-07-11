import streamlit as st
from med_explainer import get_medication_info

st.set_page_config(page_title="ClearDose – Understand Your Prescription", layout="centered")

st.title("💊 ClearDose – Understand Your Prescription")
st.markdown("Upload a medical report or prescription, or paste its content to get a simplified explanation of medications.")

uploaded_file = st.file_uploader("📄 Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
text_input = st.text_area("Or paste the prescription text here", height=150)

if st.button("Process"):
    with st.spinner("Analyzing..."):
        if text_input.strip():
            text = text_input
        else:
            text = "No valid input"
        
        st.subheader("📝 Simplified Summary")
        st.markdown("Ask your doctor if you have a history of esophageal reflux disease or if your doctor recommends a supplement.")

        st.subheader("💊 Medication Explanations")
        med_names = [line.strip() for line in text.split("\n") if line.strip()]
        for med in med_names:
            st.markdown(f"**{med}**")
            info, confidence = get_medication_info(med)
            if info:
                st.markdown(info)
            else:
                st.markdown("No description available.")
            st.caption(f"Source: {confidence}")

