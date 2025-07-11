# med_explainer.py

import re
import requests
from bs4 import BeautifulSoup

# A minimal list of common drugs to match against (expandable)
COMMON_DRUGS = [
    "paracetamol", "ibuprofen", "amoxicillin", "cetirizine", "metformin",
    "atorvastatin", "azithromycin", "omeprazole", "dolo", "pantoprazole",
    "diclofenac", "insulin", "levothyroxine", "sertraline", "alprazolam"
]

def extract_drug_names(text):
    """
    Very basic drug name extractor (can be replaced with NER later).
    """
    found = set()
    for drug in COMMON_DRUGS:
        pattern = rf"\b{re.escape(drug)}\b"
        if re.search(pattern, text, re.IGNORECASE):
            found.add(drug.lower())
    return list(found)

def fetch_drug_info_from_drugs_com(drug_name):
    """
    Fetch simplified drug info from Drugs.com.
    """
    try:
        url = f"https://www.drugs.com/{drug_name}.html"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        info_div = soup.find("div", class_="contentBox")

        if not info_div:
            return None

        paragraphs = info_div.find_all("p")
        summary = "\n\n".join(p.get_text() for p in paragraphs[:2])
        return summary.strip()

    except Exception as e:
        return None

def get_medication_info(text):
    """
    Extracts drug names from text and fetches explanations.
    """
    meds = extract_drug_names(text)
    med_info = {}
    for med in meds:
        info = fetch_drug_info_from_drugs_com(med)
        med_info[med] = info or "Information not available."
    return med_info
