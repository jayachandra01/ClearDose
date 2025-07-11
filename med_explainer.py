import requests
import time

OPENFDA_API_KEY = "hCWBxZf5AyNf60AiDYXBnQdtlxwDAtfeAgLCHvbJ"

def get_medication_info(drug_name):
    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1&api_key={OPENFDA_API_KEY}"
        retries = 3
        for i in range(retries):
            response = requests.get(url)
            if response.status_code == 429:
                time.sleep(2 ** i)  # exponential backoff
                continue
            elif response.status_code != 200:
                return None, "query_openfda"
            else:
                break

        data = response.json()
        if "results" in data:
            result = data["results"][0]
            description = result.get("description") or result.get("indications_and_usage") or result.get("purpose") or ["No info found"]
            return description[0], "query_openfda"
        else:
            return None, "query_openfda"
    except Exception:
        return None, "query_openfda"


