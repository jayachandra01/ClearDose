# med_explainer.py
import requests
import re

# Step 1: Extract drug names
def extract_drug_names(text):
    """
    Extract likely medication names by pattern-matching capitalized words and removing noise.
    """
    common_noise = {
        "doctor", "tablet", "capsule", "daily", "dr", "oral", "mg", "dose", "before",
        "after", "with", "without", "take", "once", "twice", "taper", "morning", "meals",
        "food", "evening", "bedtime", "follow", "monitor", "blood", "report", "review"
    }

    meds = set()
    lines = text.splitlines()
    for line in lines:
        if any(k in line.lower() for k in ["take", "tablet", "mg", "capsule"]):
            words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', line)  # Words starting with capital
            for word in words:
                if word.lower() not in common_noise:
                    meds.add(word)
    return list(meds)

# Step 2: Fetch info from RxNorm API
def fetch_drug_info_from_rxnorm(drug_name):
    try:
        rxcui_res = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}")
        rxcui = rxcui_res.json().get("idGroup", {}).get("rxnormId", [None])[0]
        if not rxcui:
            return None

        props_res = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/allProperties.json?prop=all")
        props = props_res.json()
        info = props.get("propConceptGroup", {}).get("propConcept", [])
        summary = "\n".join(f"- {p['propName']}: {p['propValue']}" for p in info[:5])
        return summary or "No detailed info available."
    except Exception as e:
        return f"Error fetching from RxNorm: {str(e)}"

# Step 3: Complete pipeline
def get_medication_info(text):
    meds = extract_drug_names(text)
    return {med: fetch_drug_info_from_rxnorm(med) or "No info found." for med in meds}

