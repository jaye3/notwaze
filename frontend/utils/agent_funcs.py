import streamlit as st
import requests, json

def agentInit(userData):
    st.session_state.agent_active = True

    url = "http://3.210.254.22:80/generate_route" 
    jsonData = json.dumps(userData)
    
    try:
        # Send user details to backend API to store info
        res = requests.post(url, headers={
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=jsonData)
        
        if res.status_code == 200:
            st.success(f"Response from backend: {res.json()['message']}")
            st.session_state.route = res.json()
            return res.json()
        else:
            st.error(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
    
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