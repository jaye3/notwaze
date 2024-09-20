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
from frontend.utils.render_funcs import setSearchOptions, initSession
from frontend.utils.mapping_funcs import initGdf, add_markers, add_route_lines

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
    
    dist = st.slider("Distance of your walk", 100, 7000, 2000, 100, key="distance")
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
    st.write(st.session_state.userData)

    st.button(label="Let's Go!", on_click=agentInit(st.session_state.userData), key="activate")


################################


with st.container():
    if st.session_state.agent_active:
        st.session_state.activateMap = True
        routeObj = st.session_state.route
        st.write(routeObj)

routeObj = {'total_distance': 3227.0, 'total_time': 2325.0, 'route_points': [{'name': 'User', 'type': 'User', 'latitude': 1.2973812128576165, 'longitude': 103.84959994451148}, {'name': 'HANDY RD OS', 'type': 'Park', 'latitude': 1.298995, 'longitude': 103.847793}, {'name': 'Former Convent of the Holy Infant Jesus Chapel and Caldwell House (now CHIJMES)', 'type': 'Monument', 'latitude': 1.2955939999999997, 'longitude': 103.85216}, {'name': 'ARMENIAN STREET (FCP)', 'type': 'Park', 'latitude': 1.293344, 'longitude': 103.848881}, {'name': 'National Theatre', 'type': 'Historic Site', 'latitude': 1.293482, 'longitude': 103.84459700000001}, {'name': 'End', 'type': 'End', 'latitude': 1.2888419050771158, 'longitude': 103.84509297803696}], 'route_segments': [{'from_point': {'name': 'User', 'type': 'User', 'latitude': 1.2973812128576165, 'longitude': 103.84959994451148}, 'to_point': {'name': 'HANDY RD OS', 'type': 'Park', 'latitude': 1.298995, 'longitude': 103.847793}, 'geometry': [[1.29755, 103.84973], [1.29773, 103.84951], [1.29779, 103.84955], [1.2978, 103.84953], [1.29783, 103.84949], [1.29789, 103.84941], [1.2979, 103.84938], [1.29792, 103.8494], [1.29794, 103.84938], [1.29795, 103.84935], [1.29792, 103.84934], [1.29844, 103.84872], [1.29843, 103.8487], [1.29841, 103.84869], [1.29846, 103.84867], [1.29855, 103.84857], [1.29855, 103.84852], [1.29859, 103.84854], [1.29872, 103.84863], [1.29874, 103.84864], [1.29875, 103.8486], [1.29878, 103.8485], [1.2988, 103.84844], [1.29883, 103.84832], [1.29884, 103.84829], [1.2989, 103.84824], [1.29886, 103.84824], [1.29886, 103.84814], [1.29888, 103.84813], [1.29905, 103.84782]]}, {'from_point': {'name': 'HANDY RD OS', 'type': 'Park', 'latitude': 1.298995, 'longitude': 103.847793}, 'to_point': {'name': 'Former Convent of the Holy Infant Jesus Chapel and Caldwell House (now CHIJMES)', 'type': 'Monument', 'latitude': 1.2955939999999997, 'longitude': 103.85216}, 'geometry': [[1.29905, 103.84782], [1.29888, 103.84813], [1.29886, 103.84814], [1.29886, 103.84824], [1.2989, 103.84824], [1.29884, 103.84829], [1.29883, 103.84832], [1.2988, 103.84844], [1.29878, 103.8485], [1.29875, 103.8486], [1.29874, 103.84864], [1.29872, 103.84863], [1.29859, 103.84854], [1.29855, 103.84852], [1.29855, 103.84857], [1.29846, 103.84867], [1.29841, 103.84869], [1.29843, 103.8487], [1.29844, 103.84872], [1.29792, 103.84934], [1.29795, 103.84935], [1.29794, 103.84938], [1.29792, 103.8494], [1.2979, 103.84938], [1.29789, 103.84941], [1.29783, 103.84949], [1.2978, 103.84953], [1.29779, 103.84955], [1.29773, 103.84951], [1.29726, 103.85008], [1.29722, 103.85015], [1.29728, 103.8502], [1.29726, 103.85021], [1.29714, 103.85037], [1.29698, 103.85057], [1.29683, 103.85075], [1.29672, 103.85088], [1.29664, 103.85097], [1.29661, 103.85095], [1.29658, 103.85093], [1.29658, 103.85092], [1.29647, 103.85103], [1.29649, 103.85105], [1.29652, 103.85107], [1.29654, 103.85111], [1.29653, 103.85113], [1.29621, 103.85152], [1.29605, 103.85172], [1.29602, 103.85173], [1.296, 103.85177], [1.29585, 103.85196], [1.29584, 103.85196], [1.29579, 103.85204], [1.29567, 103.85221]]}, {'from_point': {'name': 'Former Convent of the Holy Infant Jesus Chapel and Caldwell House (now CHIJMES)', 'type': 'Monument', 'latitude': 1.2955939999999997, 'longitude': 103.85216}, 'to_point': {'name': 'ARMENIAN STREET (FCP)', 'type': 'Park', 'latitude': 1.293344, 'longitude': 103.848881}, 'geometry': [[1.29567, 103.85221], [1.29579, 103.85204], [1.29584, 103.85196], [1.29585, 103.85196], [1.29549, 103.85163], [1.29545, 103.8516], [1.29537, 103.85153], [1.29531, 103.85146], [1.29511, 103.85126], [1.29501, 103.85121], [1.29489, 103.85109], [1.2948, 103.851], [1.29465, 103.85088], [1.29459, 103.85083], [1.29453, 103.85083], [1.29448, 103.85082], [1.29436, 103.85071], [1.29435, 103.85069], [1.29435, 103.85064], [1.29448, 103.8504], [1.29446, 103.85038], [1.29445, 103.85038], [1.29412, 103.8502], [1.29387, 103.85005], [1.29372, 103.85], [1.29371, 103.84998], [1.29371, 103.84993], [1.29363, 103.84985], [1.2939, 103.84936], [1.29388, 103.84928], [1.29384, 103.84926], [1.29379, 103.84923], [1.2937, 103.84918], [1.29333, 103.84898], [1.29331, 103.84897]]}, {'from_point': {'name': 'ARMENIAN STREET (FCP)', 'type': 'Park', 'latitude': 1.293344, 'longitude': 103.848881}, 'to_point': {'name': 'National Theatre', 'type': 'Historic Site', 'latitude': 1.293482, 'longitude': 103.84459700000001}, 'geometry': [[1.29331, 103.84897], [1.29323, 103.84894], [1.29314, 103.84891], [1.29311, 103.84891], [1.2931, 103.84892], [1.29303, 103.84894], [1.29296, 103.84898], [1.29288, 103.84903], [1.29285, 103.84908], [1.29264, 103.84947], [1.29262, 103.84948], [1.29245, 103.84937], [1.29243, 103.84936], [1.29242, 103.84937], [1.29241, 103.84936], [1.29237, 103.84936], [1.29231, 103.84935], [1.29219, 103.84931], [1.29192, 103.84918], [1.29179, 103.84911], [1.29171, 103.84905], [1.29169, 103.84905], [1.29129, 103.84882], [1.29128, 103.84882], [1.29085, 103.84858], [1.29063, 103.84846], [1.29045, 103.84834], [1.2904, 103.84827], [1.29038, 103.84821], [1.29036, 103.84815], [1.29035, 103.84809], [1.29035, 103.84801], [1.29036, 103.84793], [1.29037, 103.84788], [1.29044, 103.84776], [1.29054, 103.84756], [1.29061, 103.84742], [1.29062, 103.84738], [1.29071, 103.84725], [1.29071, 103.84725], [1.2908, 103.84712], [1.29089, 103.84715], [1.29095, 103.84712], [1.29103, 103.84704], [1.29116, 103.8469], [1.2912, 103.84687], [1.2912, 103.84687], [1.29121, 103.84686], [1.29122, 103.84685], [1.29132, 103.84682], [1.29146, 103.84677], [1.29152, 103.84674], [1.29158, 103.84671], [1.29167, 103.84665], [1.29177, 103.84659], [1.2918, 103.84657], [1.29183, 103.84655], [1.29188, 103.84652], [1.29192, 103.84647], [1.29196, 103.84644], [1.29206, 103.84635], [1.29211, 103.84633], [1.29215, 103.84631], [1.2922, 103.84629], [1.29225, 103.84625], [1.29228, 103.84622], [1.29231, 103.8462], [1.29235, 103.84615], [1.29242, 103.84608], [1.29256, 103.84594], [1.29264, 103.84585], [1.29278, 103.84572], [1.29282, 103.8457], [1.29287, 103.84566], [1.2929, 103.84564], [1.29292, 103.84563], [1.29298, 103.8456], [1.29309, 103.84554], [1.29319, 103.8455], [1.29326, 103.84547], [1.29336, 103.84543], [1.29345, 103.84541], [1.29345, 103.84539], [1.29346, 103.84533], [1.29347, 103.84532], [1.29349, 103.84528], [1.29349, 103.84527], [1.29351, 103.84524], [1.29351, 103.84523], [1.29353, 103.84519], [1.29354, 103.84517], [1.29356, 103.84513], [1.29358, 103.84506], [1.29358, 103.84502], [1.29357, 103.845], [1.29355, 103.84496], [1.29354, 103.84494], [1.29352, 103.8449], [1.2935, 103.84485], [1.2935, 103.84485], [1.29351, 103.84483], [1.29358, 103.84468], [1.29358, 103.84466], [1.29354, 103.84466], [1.29353, 103.84467]]}, {'from_point': {'name': 'National Theatre', 'type': 'Historic Site', 'latitude': 1.293482, 'longitude': 103.84459700000001}, 'to_point': {'name': 'End', 'type': 'End', 'latitude': 1.2888419050771158, 'longitude': 103.84509297803696}, 'geometry': [[1.2867, 103.84173], [1.28673, 103.84179], [1.28677, 103.84185], [1.28682, 103.84191], [1.28686, 103.84197], [1.28689, 103.84201], [1.2869, 103.84206], [1.2869, 103.84208], [1.28693, 103.84207], [1.28699, 103.84204], [1.28701, 103.84203], [1.28704, 103.84211], [1.28708, 103.8422], [1.2871, 103.84229], [1.28713, 103.84232], [1.28716, 103.84235], [1.28719, 103.84237], [1.28723, 103.84239], [1.28727, 103.8424], [1.28731, 103.8424], [1.28735, 103.8424], [1.28738, 103.84239], [1.28742, 103.84237], [1.28744, 103.84236], [1.28775, 103.84253], [1.28805, 103.84269], [1.28805, 103.84269], [1.28805, 103.84267], [1.28807, 103.8426], [1.28808, 103.84256], [1.2881, 103.84255], [1.28812, 103.84256], [1.28814, 103.84256], [1.28856, 103.84295], [1.28862, 103.84301], [1.28848, 103.84323], [1.28836, 103.84342], [1.28888, 103.84384], [1.28895, 103.84373], [1.2892, 103.844], [1.28911, 103.84412], [1.28858, 103.84473], [1.2885, 103.84481], [1.28866, 103.84494], [1.28865, 103.84501], [1.2887, 103.84502], [1.28873, 103.84502], [1.28885, 103.84504]]}]}
routePoints = routeObj["route_points"] # Array of dicts.

# Rendering map
if st.session_state.activateMap:
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
        [routePoints[0]["latitude"], routePoints[0]["longitude"]],
        popup='User Location',
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Add end location to the map
    folium.Marker(
        [routePoints[-1]["latitude"], routePoints[-1]["longitude"]],
        popup='End Location',
        icon=folium.Icon(color='red')
    ).add_to(m)

    # # Add POIs to the map
    # add_markers(routePoints)

    # # Add routes to the map
    # add_route_lines(routePoints)

    # Display the map
    st_data = st_folium(m, width=725)

with st.container:
    st.header("What's waiting for you on this journey?")
    st.text("🚶‍♀️🚶‍♂️\n\nHello there! I'm here to help you achieve your walking health goals by providing you with a list of interesting locations to visit in order. Here's the list:\n\n1. Start: Begin your journey at HANDY RD OS, a historic road in Singapore's Central Area.\n2. End: Next, make your way to End, a street that runs parallel to the Singapore River.\n3. Tan Si Chong Su: Take a stroll to Tan Si Chong Su, a beautiful Chinese temple that dates back to 1876.\n4. Former Convent of the Holy Infant Jesus Chapel and Caldwell House (now CHIJMES): Don't miss out on visiting this stunning complex, which was once a Catholic girls' school.\n5. CANNING RISE (FCP): End your journey at CANNING RISE (FCP), a park that offers a peaceful escape from the hustle and bustle of the city.\n\n🤩💡\n\nAs you walk, take some time to explore each location and learn about their unique histories and features. For example, did you know that Tan Si Chong Su is one of the oldest Chinese temples in Singapore, or that CHIJMES was once a school for girls run by the Sisters of the Holy Infant Jesus?\n\n💪🏃‍♀️🏃‍♂️\n\nI hope this list helps you meet your walking health goals while also allowing you to discover some of Singapore's hidden gems. If you'd like to generate another route, simply ask, and I'd be happy to summarize for you. Happy exploring! 😊🌳")
