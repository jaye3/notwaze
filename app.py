# Standard library imports
import requests, json, time

# Third-party libraries
import streamlit as st
import folium
from streamlit_folium import st_folium
from st_keyup import st_keyup
# import hydralit_components as hc

# Helper functions (local imports)
from frontend.utils.location_funcs import getCurrentLoc, getLocDetails, searchAddress
from frontend.utils.agent_funcs import activateAgent
from frontend.utils.render_funcs import setSearchOptions, initSession
from frontend.services.onemap_auth import initToken
from frontend.services.agent import agentInit

def setOptions(type, options):
    if type == "start":
        st.session_state.startOptions = options
    if type == "end":
        st.session_state.endOptions = options

##################################

# Main body
initSession()
# with hc.HyLoader('Now Loading', hc.Loaders.standard_loaders,index=1):
#     time.sleep(3)

st.image("./frontend/logo.svg", width=150)
st.title("Welcome to WalkEase - your urban walking guide on-the-go")

# Rendering in current location
userLoc = getCurrentLoc() 
userDetails = getLocDetails(userLoc)

with st.container():
    startPoint, endPoint = None, None
    start, end = userDetails["BUILDINGNAME"], ""

    startInput = st_keyup("Search for start point:", value=start, debounce=500, key="init")
    if startInput != userDetails["BUILDINGNAME"] and startInput:
        startPoint = st.selectbox(
            label="Start from:", 
            options=setSearchOptions(startInput),
            format_func=lambda x: x[0], 
            index=None, 
            key="startSelect", 
            placeholder="Select address"
            )
        if startPoint:
            start = startPoint[0]
    if startPoint:
        st.write(startPoint)

    endInput = st_keyup("Search for end point:", value=end, debounce=500)
    if endInput:
        endPoint = st.selectbox(
            label="End at:", 
            options=setSearchOptions(endInput),
            format_func=lambda x: x[0], 
            index=None, 
            key="endSelect", 
            placeholder="Select address"
            )
        if endPoint:
            end = endPoint[0]

    dist = st.slider("Distance of your walk", 100, 7000, 1000, 100, key="distance")

    st.button(label="Let's Go!", on_click=lambda: activateAgent(startPoint, endPoint, dist), key="activate")



################################

with st.container():
    if st.session_state.agent_active:
        st.header("Personalise your route with Waz, our chatbot!")
        agentInit()
        

# Rendering map
# if st.session_state.start != userLocName:

# # placeholder for testing

# # Create a folium map centered around the user's location
# m = folium.Map(
#     location=[user_location.y, user_location.x],
#     zoom_start=100,
#     control_scale=True
#     )

# # Add user location to the map
# folium.Marker([user_location.y, user_location.x], popup='User Location', icon=folium.Icon(color='red')).add_to(m)

# last_point = user_location
# # # Add POIs to the map
# for idx, row in intersecting_pois.iterrows():
#     folium.Marker([row.geometry.y, row.geometry.x], popup=row['NAME']).add_to(m)
#     folium.PolyLine([[last_point.y, last_point.x], [row.geometry.y, row.geometry.x]]).add_to(m)

# # Add buffer to the map
# folium.GeoJson(user_buffer.to_crs(epsg=4326).geometry).add_to(m)
