import time
from streamlit_js_eval import get_geolocation
from frontend.services.onemap_auth import getResponse

def getCurrentLoc():
    currentLoc = get_geolocation()
    time.sleep(1)
    if currentLoc == None:
        return None

    details = currentLoc["coords"] 
    coords = [details["latitude"], details["longitude"]]
        
    return coords

def getLocDetails(loc): # takes in a lat-long pair
    lat, long = loc[0], loc[1]

    url = f"https://www.onemap.gov.sg/api/public/revgeocode?location={lat},{long}&buffer=40&addressType=All&otherFeatures=N"
    res = getResponse(url)
    locDetails = res["GeocodeInfo"][0]

    return locDetails

def searchAddress(search):
    keystr = search.replace(" ", "+")
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={keystr}&returnGeom=Y&getAddrDetails=Y"
    res = getResponse(url)
        
    return res["results"]