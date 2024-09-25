from frontend.services.onemap_auth import initToken
from frontend.utils.location_funcs import searchAddress
import streamlit as st
import os

def initSession():
    if "ONEMAP_API_KEY" not in st.session_state:
        initToken()
    if "submitted" not in st.session_state:
        st.session_state.submitted = False 
    if 'agent_active' not in st.session_state:
        st.session_state.agent_active = False
    if "start" not in st.session_state:
        st.session_state.start = None
    if "end" not in st.session_state:
        st.session_state.end = None   
    if "startLoc" not in st.session_state:
        st.session_state.startLoc = None  
    if "endLoc" not in st.session_state:
        st.session_state.endLoc = None  
    if "route" not in st.session_state:
        st.session_state.route = None  
    if "activateMap" not in st.session_state:
        st.session_state.activateMap = None 
    if "valid_form" not in st.session_state:
        st.session_state.valid_form = None 
    if "route_success" not in st.session_state:
        st.session_state.route_success = None
    if "activate_summary" not in st.session_state:
        st.session_state.activate_summary = None



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

