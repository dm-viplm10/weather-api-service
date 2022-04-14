from weather_api_service import db, secret_key, encrypt, decrypt
from weather_api_service.models.User import User
from weather_api_service.models.HttpResponse import HttpResponse
import json
from pathlib import Path

def ReadCountryFile() -> dict:
    countryDict = {}
    mod_path = Path(__file__).parent
    rel_path = '../data/country_data.json'
    path =  (mod_path / rel_path).resolve()
    
    with open(path, 'r', encoding='utf-8') as f:
        cont = f.read()
    data = json.loads(cont)
    
    for elem in data:
        if elem['country'] in list(countryDict.keys()):
            countryDict[elem['country']].append(elem['name'])
        else:
            countryDict[elem['country']] = [elem['name']]

    return countryDict