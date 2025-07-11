# med_explainer.py (RxNorm API version)

import requests
import re

EXCLUSION_WORDS = {"doctor", "tablet", "capsule", "daily", "dr", "oral", "mg", "dose", "before", "after", "with", "without"}

def extract_drug_names(text):
    """
    Extracts potential medication names using simple heuristics.
    """
    meds = set()
    lines = text.lower().splitlines()
    for line in lines:
        if any(k in line for k in ["take", "tablet", "mg", "capsule"]):
            words = re.findall(r'\b[a-zA-Z]{4,}\b', line)
            for word in words:
                if word not in EXCLUSION_WORDS:
                    meds.add(word)
    return list(meds)

def fetch_drug_info_from_rxnorm(drug_name):
    """
    Fetches drug explanation using trusted RxNorm API.
    """
    try:
        # Step 1: Get RXCUI ID
        rxcui_res = requests.get(
            f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}"
        )
        rxcui = rxcui_res.json().get("idGroup", {}).get("rxnormId", [None])[0]
        if not rxcui:
            return None

        # Step 2: Get drug properties
        props_res = requests.get(
            f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/allProperties.json?prop=all"
        )
        props = props_res.json()
        info = props.get("propConceptGroup", {}).get("propConcept", [])
        summary = "\n".join(f"- {p['propName']}: {p['propValue']}" for p in info[:5])
        return summary or "No detailed info available."

    except Exception as e:
        return f"Error: {str(e)}"

def get_medication_info(text):
    """
    Extracts drug names and fetches explanations from RxNorm API.
    """
    meds = extract_drug_names(text)
    return {med: fetch_drug_info_from_rxnorm(med) or "No info found." for med in meds}


