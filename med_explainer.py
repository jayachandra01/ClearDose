# med_explainer.py

from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# Load Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_drug_names(text):
    """
    Uses Hugging Face NER to extract named entities, filtering for likely drug names.
    """
    entities = ner_pipeline(text)
    drug_names = set()

    for ent in entities:
        word = ent['word'].strip()
        label = ent['entity_group']
        # Heuristic filter: keep only 'MISC' or 'ORG' or proper nouns likely to be drugs
        if label in ["ORG", "MISC", "PER", "LOC"]:
            if len(word) > 3 and word.lower() not in ['tablet', 'doctor', 'mg', 'dose', 'dr']:
                drug_names.add(word.lower())

    return list(drug_names)

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

