# summarizer.py

from transformers import pipeline
import torch

# Load once globally
device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", model="google/flan-t5-base", device=device)

def simplify_text(text: str, max_tokens: int = 512) -> str:
    """
    Summarizes medical text into layman-friendly language using FLAN-T5.
    """
    # Truncate if needed (FLAN-T5 has 512 token limit)
    if len(text.split()) > max_tokens:
        text = " ".join(text.split()[:max_tokens])

    prompt = f"Summarize the following medical text in simple language:\n\n{text}"

    try:
        result = summarizer(prompt, max_length=200, min_length=30, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        return f"⚠️ Summarization failed: {str(e)}"
