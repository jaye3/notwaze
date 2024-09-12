from services.onemap_auth import initToken
from utils.location_funcs import searchAddress
import streamlit as st
import os

def initSession():
    if 'agent_active' not in st.session_state:
        st.session_state.agent_active = False
    if "ONEMAP_API_KEY" not in os.environ:
        initToken()


def setSearchOptions(loc):
    res = searchAddress(loc)
    labels = [x["ADDRESS"] for x in res]
    coords = [(y["LATITUDE"], y["LONGITUDE"]) for y in res]
    options = list(zip(labels, coords))
    return options
