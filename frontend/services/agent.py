import streamlit as st
import boto3
import requests
from frontend.utils.agent_funcs import agentRouting

def activateAgent():
    region = "us-east-1"
    session = boto3.Session(region_name=region)

    # Initialize chat history with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "Waz",
            "content": "Hello! I got all the info you just entered! Here's what I got for you:"
        }]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
        route_res = agentRouting()

        # Check if a valid route is returned
        if 'route_points' in route_res and len(route_res['route_points']) > 0:
            # Get the single route point
            route_point = route_res['route_points'][0]
            options_message = f"Here is your route option:\n- {route_point['name']} (Lat: {route_point['latitude']}, Lon: {route_point['longitude']})"
            st.chat_message("assistant").markdown(options_message)

            # Create a button for the user to confirm their selection
            if st.button("Select this route"):
                selected_route = f"You selected: {route_point['name']}"
                st.chat_message("user").markdown(selected_route)

                # Add user input to chat history
                st.session_state.messages.append({"role": "user", "content": selected_route})

        else:
            st.chat_message("assistant").markdown("Sorry, no valid routes found.")
