# Standard library imports
import requests, json, time

# Third-party libraries
import streamlit as st
from st_keyup import st_keyup
import folium

# Helper functions (local imports)
from frontend.utils.location_funcs import getCurrentLoc, getLocDetails, searchAddress
from frontend.utils.agent_funcs import agentInit
from frontend.utils.render_funcs import setSearchOptions, initSession
from frontend.services.onemap_auth import initToken
from frontend.utils.mapping_funcs import initGdf, add_markers, add_route_lines
from frontend.services.agent import activateAgent

def setOptions(type, options):
    if type == "start":
        st.session_state.startOptions = options
    if type == "end":
        st.session_state.endOptions = options

##################################

# Setup Page and Session
initSession()

st.set_page_config(
    page_title="WalkEaze",
    layout="wide"
)

# Rendering in current location
userLoc = getCurrentLoc() 
if userLoc != None:
    userDetails = getLocDetails(userLoc)

if st.session_state.start == None and userLoc != None:
    # st.write(st.session_state.start)
    st.session_state.startLoc, st.session_state.endLoc = userLoc, userLoc
    st.session_state.start, st.session_state.end = userDetails["BUILDINGNAME"], userDetails["BUILDINGNAME"]

st.image("./frontend/logo.svg", width=150)
st.header("Welcome to WalkEaze - your urban walking guide on-the-go")

with st.container():
    startInput = st_keyup("Search for start point:", value=st.session_state.start, debounce=500, key="init")
    if startInput != st.session_state.start and startInput:
        startPoint = st.selectbox(
            label="Start from:", 
            options=setSearchOptions(startInput),
            format_func=lambda x: x[0], 
            index=None, 
            key="startSelect", 
            placeholder="Select address"
            )
        if startPoint:
            st.session_state.start = startPoint[0]
            st.session_state.startLoc = startPoint[1]

    endInput = st_keyup("Search for end point:", value=st.session_state.end, debounce=500, key="endInit")
    if endInput != st.session_state.end and endInput:
        endPoint = st.selectbox(
            label="End at:", 
            options=setSearchOptions(endInput),
            format_func=lambda x: x[0], 
            index=None, 
            key="endSelect", 
            placeholder="Select address"
            )
        if endPoint:
            st.session_state.end = endPoint[0]
            st.session_state.endLoc = endPoint[1]
    
    dist = st.slider("Distance of your walk", 100, 7000, 1000, 100, key="distance")
    radius = dist // 2

    num_pois = st.slider("How many places would you like to visit on your walk?", 1, 10, 5, key="pois")

    poi_types = st.multiselect(
        label="What would you like to see? (choose one or more options)",
        options=[
                ['Monuments', 'monument'], 
                ['Historic Sites', 'historicSite'], 
                ['Parks', 'park'], 
                ['Museums', 'museum']
            ],
        format_func=lambda x:x[0],
    )
    poi_types = [x[1] for x in poi_types]

    includeAmenity = st.checkbox(
        label="Include amenities (i.e. toilets) in the route",
    )
    isBarrierFree = st.checkbox(
        label="Prefer to avoid barriers (e.g. stairs) along the route"
    )
    

    userData = {
        "user_location": st.session_state.startLoc,
        "end_location": st.session_state.endLoc,
        "max_route_length": dist, 
        "search_radius": radius,
        "num_POIs": num_pois,
        "poi_types": poi_types,
        "amenity": includeAmenity,
        "barrier_free": isBarrierFree
    }
    st.write(userData)

    st.button(label="Let's Go!", on_click=lambda: agentInit(userData), key="activate")


################################


with st.container():
    if st.session_state.agent_active:
        st.header("Personalise your route with Waz, our chatbot!")
        activateAgent()
    
# Rendering map
if st.session_state.activateMap:

    # The line below is to import the CSS from font-awesome -- to use their icons (refer to icon_dict in function add_poi_markers)
    html = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'

    # Define a map boundary so user cannot drag map out too far (Hard-coded)
    min_lon, max_lon = 102.6920, 105.0920
    min_lat, max_lat = 1.0305, 1.5505

    route_gdf = initGdf(st.session_state.route)

    # Create a folium map centered around the user's location
    m = folium.Map(
        location=(user_gdf.iloc[0].geometry.y, user_gdf.iloc[0].geometry.x),
        zoom_start=15,
        control_scale=True,
        tiles='Cartodb Positron',
        max_bounds=True,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        )

    # # Add buffer to the map
    # folium.GeoJson(search_buffer_gdf.geometry,
    #             style_function=lambda x: {
    #                 'fillOpacity': 0.1       # Set fill opacity to 10%
    #                 }
    #                 ).add_to(m)

    # # Add locactions of stairs in red
    # folium.GeoJson(
    #     avoidance_buffer_gdf.geometry,
    #     style_function=lambda x: {'color': 'magenta'},
    #     tooltip='Stairs'
    #     ).add_to(m)


    # Add user location to the map
    folium.Marker(
        [user_gdf.iloc[0].geometry.y, user_gdf.iloc[0].geometry.x],
        popup='User Location',
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Add end location to the map
    folium.Marker(
        [end_gdf.iloc[0].geometry.y, end_gdf.iloc[0].geometry.x],
        popup='End Location',
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Add POIs to the map
    add_markers(route_gdf)

    # Add routes to the map
    add_route_lines(route_gdf)

    # Display the map
    m
