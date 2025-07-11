from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re

# Load Hugging Face medical NER model
try:
    ner_pipeline = pipeline("ner", model="d4data/biomedical-ner-all", grouped_entities=True)
except:
    ner_pipeline = None  # fallback if load fails

EXCLUSION_WORDS = {"doctor", "mg", "tablet", "capsule", "daily", "take", "breakfast", "dinner", "liver", "results", "dr", "crp", "monitor"}

def extract_drug_names(text):
    """
    Hybrid drug name extractor using biomedical NER with fallback to regex.
    """
    meds = set()

    # Step 1: Try biomedical NER
    if ner_pipeline:
        try:
            entities = ner_pipeline(text)
            for ent in entities:
                word = ent['word'].strip().lower()
                if word not in EXCLUSION_WORDS and len(word) > 3 and word.isalpha():
                    meds.add(word)
        except:
            pass

    # Step 2: Fallback – regex + heuristics
    if not meds:
        lines = text.lower().splitlines()
        for line in lines:
            if any(k in line for k in ["take", "tablet", "mg", "capsule"]):
                words = re.findall(r'\b[a-zA-Z]{5,}\b', line)
                for word in words:
                    if word not in EXCLUSION_WORDS:
                        meds.add(word)

    return list(meds)

def fetch_drug_info_from_drugs_com(drug_name):
    """
    Scrape basic info from Drugs.com
    """
    try:
        url = f"https://www.drugs.com/{drug_name.lower().replace(' ', '-')}.html"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        box = soup.find("div", class_="contentBox")
        if not box:
            return None

        ps = box.find_all("p")
        return "\n\n".join(p.get_text() for p in ps[:2])
    except:
        return None

def get_medication_info(text):
    """
    Extracts drug names and fetches explanations.
    """
    meds = extract_drug_names(text)
    return {med: fetch_drug_info_from_drugs_com(med) or "No info found." for med in meds}


