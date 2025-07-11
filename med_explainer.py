import requests
import logging
from bs4 import BeautifulSoup

# Set up logging for missing or failed lookups
logging.basicConfig(filename='drug_lookup.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def query_rxnorm(drug):
    try:
        response = requests.get(
            f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug}')
        rxcui = response.json().get('idGroup', {}).get('rxnormId', [None])[0]
        if rxcui:
            desc = requests.get(
                f'https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json')
            return desc.json().get('properties', {}).get('synonym', 'No description available.')
    except Exception as e:
        logging.warning(f'RxNorm failed for {drug}: {e}')
    return None

def query_openfda(drug):
    try:
        response = requests.get(
            f'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{drug}"&limit=1')
        data = response.json().get('results', [{}])[0]
        return data.get('description', ['No description available.'])[0]
    except Exception as e:
        logging.warning(f'OpenFDA failed for {drug}: {e}')
    return None

def query_medlineplus(drug):
    try:
        url = f'https://medlineplus.gov/druginfo/meds/{drug.lower()[:3]}.html'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        desc_tag = soup.find('div', class_='section-body')
        return desc_tag.text.strip() if desc_tag else None
    except Exception as e:
        logging.warning(f'MedlinePlus failed for {drug}: {e}')
    return None

def get_medication_info(drug):
    sources = [query_rxnorm, query_openfda, query_medlineplus]
    for source in sources:
        info = source(drug)
        if info:
            return {"info": info, "confidence": f"Source: {source.__name__}"}
    logging.info(f'Drug not found in any source: {drug}')
    return {"info": "No information found.", "confidence": "None"}


