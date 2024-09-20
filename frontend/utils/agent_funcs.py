import streamlit as st
import requests, json, os

def agentInit(userData):
    st.session_state.agent_active = True

    import requests

    # Define the URL endpoint
    url = "http://3.210.254.22:80/generate_route"

    # Define the headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # Define the JSON data to send in the POST request
    data = {
        "user_location": [103.84959994451148, 1.2973812128576168],
        "end_location": [103.84509297803696, 1.2888419050771158],
        "search_radius": 500,
        "num_POIs": 5,
        "max_route_length": 3000,
        "poi_types": ["monument", "historicSite", "park", "museum"],
        "amenity": True,
        "barrier_free": True
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())  # Assuming the response is in JSON format
    else:
        print(f"Failed with status code {response.status_code}")
        print("Response:", response.text)

    
    return 

def generateSummary():
    url = "http://3.210.254.22/generate-summary" 
    
    try:
        # Send user details to backend API to store info
        res = requests.get(url)

        if res.status_code == 200:
            st.success(f"Response from backend: {res.json()['message']}")
            return res.json()
        else:
            st.error(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
    
    return 