import requests, os, time, streamlit
from dotenv import load_dotenv
from streamlit_js_eval import get_geolocation
from frontend.services.onemap_auth import getResponse

def getCurrentLoc():
    currentLoc = get_geolocation()
    while currentLoc is None:
        time.sleep(0.5)
    currentLoc = currentLoc["coords"] 
        
    return currentLoc

def getLocDetails(loc): # takes in a lat-long dict key-value pair
    lat, long = loc["latitude"], loc["longitude"]

    url = f"https://www.onemap.gov.sg/api/public/revgeocode?location={lat},{long}&buffer=40&addressType=All&otherFeatures=N"
    res = getResponse(url)
    locDetails = res["GeocodeInfo"][0]

    return locDetails

def searchAddress(search):
    keystr = search.replace(" ", "+")
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={keystr}&returnGeom=Y&getAddrDetails=Y"
    res = getResponse(url)
        
    return res["results"]