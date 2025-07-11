# med_explainer.py

import spacy
import requests
from bs4 import BeautifulSoup

# Load NER model from SciSpacy
nlp = spacy.load("en_ner_bc5cdr_md")

def extract_drug_names(text):
    """
    Uses SciSpacy biomedical NER to extract drug names from text.
    """
    doc = nlp(text)
    drugs = set()
    for ent in doc.ents:
        if ent.label_ == "CHEMICAL":
            drugs.add(ent.text.lower())
    return list(drugs)

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
        from bs4 import BeautifulSoup
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
    Extracts drug names and fetches info for each.
    """
    meds = extract_drug_names(text)
    return {med: fetch_drug_info_from_drugs_com(med) or "No info found." for med in meds}
