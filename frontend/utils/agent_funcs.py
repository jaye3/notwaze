import streamlit as st
import requests

def agentInit(userData):
    st.session_state.agent_active = True

    # Define the URL endpoint
    url = "http://3.210.254.22:80/generate_route"

    # Define the headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    #Define the JSON data to send in the POST request
    data = {
        "user_location": [userData['user_location'][1], userData['user_location'][0]],
        "end_location": [userData['end_location'][1], userData['end_location'][0]],
        "search_radius": userData['search_radius'],
        "num_POIs": userData['num_POIs'],
        "max_route_length": userData['max_route_length'],
        "poi_types": userData["poi_types"],
        "amenity": userData['amenity'],
        "barrier_free": userData['barrier_free']
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # st.success("Success!")
        st.session_state.route = response.json()
        st.session_state.route_success = True
        # st.write(response.json())
        return response.json()  # Assuming the response is in JSON format
    else:
        # st.error(f"Failed with status code {response.status_code}")
        st.session_state.route_success = False
    
    return 

def generateSummary():
    url = "http://3.210.254.22/generate-summary" 
    
    try:
        # Send user details to backend API to store info
        res = requests.get(url)

        if res.status_code == 200:
            # st.success(f"Response from backend: {res.status_code}")
            res = res.json()
            summary = next(iter(res.values()))
            return summary
        else:
            return None
            # st.error(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        return None
        # st.error(f"Request failed: {e}")
    
