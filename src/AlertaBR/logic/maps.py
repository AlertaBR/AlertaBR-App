import requests.api as req
import src.AlertaBR.logic.verifications as verif
import src.AlertaBR.logic.climatic as clima

def formatAddress(street):
    if ' ' not in street:
        return street
    
    street = verif.replaceString(street, '+')
    
    return street

def getStreetResponse(userInput):
    endpoint = f"https://nominatim.openstreetmap.org/search?q={userInput}&countrycodes=br&limit=1&format=json"
    
    headers = {'User-Agent': 'my user agent'} # Os header devem ser definidos para que a requisição seja feita no endereço certo
    
    response = req.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()[0] if len(response.json()) > 0 else {}
    return {}