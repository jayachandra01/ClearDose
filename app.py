import gradio as gr
from transformers import pipeline

# Load FLAN-T5 small model (lightweight and free-tier friendly)
model = pipeline("text2text-generation", model="google/flan-t5-small")

def explain_medication(med_name, tone):
    prompt = f"Explain the usage, dosage, and side effects of {med_name} in a {tone} tone. Keep it simple and clear for a patient. End with: 'This is not medical advice. Always consult a doctor.'"
    result = model(prompt, max_new_tokens=256, do_sample=False)
    return result[0]['generated_text']

def explain_test_result(test_info, tone):
    prompt = f"Explain the meaning of this medical test result: {test_info}. Use a {tone} tone. Be clear and reassuring. End with: 'This is not medical advice. Always consult a doctor.'"
    result = model(prompt, max_new_tokens=256, do_sample=False)
    return result[0]['generated_text']

with gr.Blocks() as demo:
    gr.Markdown("# 🩺 ClearDose - GenAI Medical Assistant")
    gr.Markdown("Explain medications and lab test results in plain language.")

    with gr.Tab("💊 Medication Explainer"):
        med_input = gr.Textbox(label="Enter medicine (e.g. 'Paracetamol 650mg')")
        tone_input = gr.Radio(["simple", "professional", "empathetic"], label="Tone", value="simple")
        med_button = gr.Button("Explain")
        med_output = gr.Textbox(label="Explanation")
        med_button.click(fn=explain_medication, inputs=[med_input, tone_input], outputs=med_output)

    with gr.Tab("🧪 Test Result Explainer"):
        test_input = gr.Textbox(label="Enter test result (e.g. 'HbA1c 8.3%')")
        tone_input_2 = gr.Radio(["simple", "professional", "empathetic"], label="Tone", value="simple")
        test_button = gr.Button("Explain")
        test_output = gr.Textbox(label="Explanation")
        test_button.click(fn=explain_test_result, inputs=[test_input, tone_input_2], outputs=test_output)

demo.launch()