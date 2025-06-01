import requests.api as req
import verifications as verif

def formatAddress(street):
    if ' ' not in street:
        return street
    
    street = verif.replaceString(street)
    
    return street

def getStreetResponse(userInput):
    headers = {'User-Agent': 'my user agent'} # The problem was that the geocode function was directly calling the nominatim API rather than using the nominatim_request function which handles all the caching, user-agent, referer, etc.
    endpoint = f"https://nominatim.openstreetmap.org/search?q={userInput}&countrycodes=br&limit=1&format=json"
    
    response = req.get(endpoint, headers=headers)
    return response.json()[0]

userInput = input('Digite um endereço: ')
userInput = formatAddress(userInput)
dictStreet = getStreetResponse(userInput)
