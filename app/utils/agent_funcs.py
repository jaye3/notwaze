import streamlit as st

def activateAgent(startDetails, endDetails, distance):
    #start and end details are a tuple of (layman address, (lat, long))
    st.session_state.agent_active = True
    # either here or in the agent file, we pass in the information 

    return