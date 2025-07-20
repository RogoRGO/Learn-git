import requests
import json

API_URL = "https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva"
HEADERS = {"Content-Type": "application/json"}

def construieste_payload(cuiuri, data_interogare): # Costruiesc payload-ul JSON pentru request
    return [{"cui": int(cui), "data": data_interogare} for cui in cuiuri]



def trimite_request(payload): # Trimit POST request catre API-ul ANAF cu payload-ul. Returneaza JSON-ul raspuns sau None la eroare
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request esuat. Cod status: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Eroare la trimiterea request-ului: {e}")
        return None