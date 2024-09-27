from frontend.services.onemap_auth import initToken
from frontend.utils.location_funcs import searchAddress
import streamlit as st

def initSession():
    if "ONEMAP_API_KEY" not in st.session_state:
        initToken()

    defaults = {
        "submitted": False,
        "agent_active": False,
        "start": None,
        "end": None,
        "startLoc": None,
        "endLoc": None,
        "route": None,
        "activateMap": None,
        "valid_form": None,
        "route_success": None,
        "activate_summary": None,
        "location_permit": False,
        "use_curr_start": False,
        "use_curr_end": False,
        "route_error_count": 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setSearchOptions(loc):
    res = searchAddress(loc)
    labels = [x["ADDRESS"] for x in res]
    coords = [[float(y["LATITUDE"]), float(y["LONGITUDE"])] for y in res]
    options = list(zip(labels, coords))
    return options

def checkData():
    st.session_state.submitted = True
    data = st.session_state.userData    

    if None not in data.values():
        st.session_state.valid_form = True
        # resets the button every time it is pressed
        st.session_state.route_success = None
        st.session_state.generate_summary = None

