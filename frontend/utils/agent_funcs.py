import streamlit as st
import requests

def agentInit(startDetails, endDetails, distance):
    #start and end details are a tuple of (layman address, (lat, long))
    st.session_state.agent_active = True
    url = "http://127.0.0.1:8000/docs/collect-user-data" #currently localhost

    radius = distance // 2
    data = {
            "user_location": startDetails,
            "end_location": endDetails,
            "search_radius": radius ,
            "num_POIs": 5,
            "max_route_length": distance
        }
    try:
        # Send user details to backend API to store info
        res = requests.post(url, data)

        if res.status_code == 200:
            st.success(f"Response from backend: {res.json()['message']}")
        else:
            st.error(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
    
    return