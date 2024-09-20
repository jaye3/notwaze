import streamlit as st
import requests

def agentInit(userData):
    #start and end details are a tuple of (layman address, (lat, long))
    st.session_state.agent_active = True
    st.session_state.page = "chatbot"

    url = "https://ec2-100-26-41-70.compute-1.amazonaws.com:80/collect-user-data" 

    radius = userData["max_route_length"] // 2
    userData["search_radius"] = radius
    userData["num_POIs"] = 5
    st.write(userData)
    
    try:
        # Send user details to backend API to store info
        res = requests.post(url, json=userData)

        if res.status_code == 200:
            st.success(f"Response from backend: {res.json()['message']}")
        else:
            st.error(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
    
    return

# def agentRouting():
#     url = "http://ec2-100-26-41-70.compute-1.amazonaws.com:80/generate-route" 
#     try:
#         # Send user details to backend API to store info
#         res = requests.post(url)

#         if res.status_code == 200:
#             st.success(f"Response from backend: {res.json()['message']}")
#         else:
#             st.error(f"Error: {res.status_code} - {res.text}")
#     except Exception as e:
#         st.error(f"Request failed: {e}")
    
#     return
    
