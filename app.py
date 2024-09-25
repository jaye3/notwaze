# Standard library imports
import requests, json, time

# Third-party libraries
import streamlit as st
from st_keyup import st_keyup
import folium
from streamlit_folium import st_folium


# Helper functions (local imports)
from frontend.utils.location_funcs import getCurrentLoc, getLocDetails, searchAddress
from frontend.utils.agent_funcs import agentInit, generateSummary
from frontend.utils.render_funcs import setSearchOptions, initSession, checkData
from frontend.utils.mapping_funcs import add_markers, add_route_lines

def setOptions(type, options):
    if type == "start":
        st.session_state.startOptions = options
    if type == "end":
        st.session_state.endOptions = options

# Function to scroll to the bottom
def scrollToBottom():
    st.components.v1.html(
        """
        <script>
        window.scrollTo(0, document.body.scrollHeight);
        </script>
        """,
        height=0,
    )

##################################

# Setup page configuration
st.set_page_config(
    page_title="Walk Eaze",
    layout="wide"
)

# Initialising session (run only on-load)
if 'session_start' not in st.session_state:
    st.session_state['session_start'] = True
    initSession()

# Rendering in current location
userLoc = getCurrentLoc() 
if userLoc != None:
    userDetails = getLocDetails(userLoc)

if st.session_state.start == None and userLoc != None:
    st.session_state.startLoc, st.session_state.endLoc = userLoc, userLoc
    st.session_state.start, st.session_state.end = userDetails["BUILDINGNAME"], userDetails["BUILDINGNAME"]

st.image("./frontend/logo.svg", width=150)
st.header("Welcome to Walk Eaze - your urban walking guide on-the-go")

# Getting start location from user (pre-populated if Location is permitted)
st.write("Let's get you started! Please enter your start point:")
startInput = st_keyup("Search for start point:", value=st.session_state.start, debounce=500, key="startInit")

    # Error message handling for empty field input
if st.session_state.submitted and st.session_state.start == None:
    st.error("Please enter a start point.", icon=":material/error:")

    # Load in address options when user types in the input above
if startInput != st.session_state.start:
    startPoint = st.selectbox(
        label="Start from:", 
        options=setSearchOptions(startInput),
        format_func=lambda x: x[0], 
        index=None, 
        key="startSelect", 
        placeholder="Select address"
        )
    
    # Updating session variables with user's choice
    if startPoint:
        st.session_state.start = startPoint[0]
        st.session_state.startLoc = startPoint[1]
    else: 
        st.caption("Please select a valid start address from the options given.")

if st.session_state.startLoc != None:
    st.divider() ########################################################
    st.write("Great! Where would you like to walk to?")
# Getting end location from user (pre-populated as Start location if none specified)
    endInput = st_keyup("Search for end point:", value=st.session_state.end, debounce=1100, key="endInit")

        # Error message handling for empty field input
    if st.session_state.submitted and st.session_state.end is None:
        st.error("Please enter an end point.", icon=":material/error:")

        # Load in address options when user types in the input above
    if endInput != st.session_state.end and endInput:
        endPoint = st.selectbox(
            label="End at:", 
            options=setSearchOptions(endInput),
            format_func=lambda x: x[0], 
            index=None, 
            key="endSelect", 
            placeholder="Select address"
            )
        
        # Updating session variables with user's choice
        if endPoint:
            st.session_state.end = endPoint[0]
            st.session_state.endLoc = endPoint[1]
        else:
            st.caption("Please select a valid end address from the options given.")
    

if st.session_state.endLoc != None:
    st.divider() ########################################################
    st.write("Feel free to customise your trail as you'd like!")

    dist = st.slider("Distance of your walk (km):", 100, 7000, 2000, 100, key="distance")
    radius = dist // 2

    num_pois = st.slider("How many places would you like to visit on your walk?", 1, 8, 5, key="pois")

    poi_types = st.multiselect(
        label="What would you like to see? (choose one or more options)",
        options=[
                ['Monuments', 'monument'], 
                ['Historic Sites', 'historicSite'], 
                ['Parks', 'park'], 
                ['Museums', 'museum']
            ],
        default=[
                ['Historic Sites', 'historicSite'], 
                ['Parks', 'park']
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

    # Load user input data into dictionary for function-passing
    st.session_state.userData = {
        "user_location": st.session_state.startLoc,
        "end_location": st.session_state.endLoc,
        "max_route_length": dist, 
        "search_radius": radius,
        "num_POIs": num_pois,
        "poi_types": poi_types,
        "amenity": includeAmenity,
        "barrier_free": isBarrierFree
    }

    st.button(label="Let's Go!", on_click=checkData, key="activate")

################################
st.divider()

# Only loads the agent functions & map if user inputs are all valid
if st.session_state.valid_form:
    st.header("Your route, at a glance:")
    if st.session_state.route_success is None:
        with st.spinner("Creating your route..."):
            st.session_state.route_success = agentInit(st.session_state.userData)

    if st.session_state.route_success:
        st.session_state.activateMap = True
    else:
        st.error("We had some issues generating your route. \nMaybe try reducing the number of places to visit, or increase the distance of your walk?", 
        icon=":material/fmd_bad:")

# Rendering map
if st.session_state.activateMap:
    routeObj = st.session_state.route
    routePoints = routeObj["route_points"] # Array of dicts.
    routeSegments = routeObj['route_segments']
    # The line below is to import the CSS from font-awesome -- to use their icons (refer to icon_dict in function add_poi_markers)
    html = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'

    # Define a map boundary so user cannot drag map out too far (Hard-coded)
    min_lon, max_lon = 102.6920, 105.0920
    min_lat, max_lat = 1.0305, 1.5505

    # Create a folium map centered around the user's location
    m = folium.Map(
        location=(routePoints[0]["latitude"], routePoints[0]["longitude"]),
        zoom_start=15,
        control_scale=True,
        tiles='Cartodb Positron',
        max_bounds=True,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        )

    # # Add locactions of stairs in red
    # folium.GeoJson(
    #     avoidance_buffer_gdf.geometry,
    #     style_function=lambda x: {'color': 'magenta'},
    #     tooltip='Stairs'
    #     ).add_to(m)
    
    for i in range(len(routeSegments)):
        indiv_segment = routeSegments[i]
        folium.PolyLine(
            locations=indiv_segment["geometry"],
            color="blue",
            weight=5,
            opacity=0.6
        ).add_to(m)
    

    for i in range(len(routePoints)):
        folium.Marker(
            [routePoints[i]["latitude"], routePoints[i]["longitude"]],
            popup='User Location',
            icon=folium.Icon(color='red')
        ).add_to(m)

    # Add POIs to the map
    # add_markers(routePoints)

    # # Add routes to the map
    # add_route_lines(routePoints)

    # Display the map
    st_data = st_folium(m, width=725)
    st.session_state.activate_summary = True
    
if st.session_state.activate_summary:
    st.header("What's waiting for you on this journey?")
    with st.spinner("Generating summary..."):
        summary = generateSummary()
        if summary != None:
            st.write(summary)
        else:
            st.write("We had some trouble generating a summary for this route, but rest assured it'll be a fun one!")

st.write("Checking scroll conditions...")
st.write("Start Location:", st.session_state.startLoc)
st.write("End Location:", st.session_state.endLoc)
st.write("Map Activated:", st.session_state.activateMap)
st.write("Summary Activated:", st.session_state.activate_summary)

if st.session_state.startLoc != None or st.session_state.endLoc is not None or st.session_state.activateMap or st.session_state.activate_summary:
    st.write("Scrolling to bottom...")
    scrollToBottom()