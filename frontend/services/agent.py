import streamlit as st
import boto3, json

import requests

def activateAgent():
    region = "us-east-1"
    session = boto3.Session(region_name=region)

    # Initialize chat history with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "Waz",
            "content": "Hello! I got all the info you just entered! Here's what I got for you:"
        }]

    # Initialize session id
    if 'sessionId' not in st.session_state:
        st.session_state['sessionId'] = ""

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate route when chatbot initializes
    url = "http://3.89.63.81:80/generate-route"  

    try:
        response = requests.post(url)  
        st.write(response)
        route_response = response.json()  # Parse the JSON response
        st.session_state.route = response.json()

        # Check if a valid route is returned
        if 'route_points' in route_response:
            # Display route options in chat
            route_points = route_response['route_points']
            options_message = "Here are your route options:\n"
            for point in route_points:
                options_message += f"- {point['name']} (Lat: {point['latitude']}, Lon: {point['longitude']})\n"

            st.chat_message("assistant").markdown(options_message)
        else:
            st.chat_message("assistant").markdown("Sorry, no valid routes found.")

    except requests.exceptions.RequestException as e:
        st.chat_message("assistant").markdown(f"Error connecting to the route generation service: {str(e)}")

    # React to user input
    if prompt := st.chat_input("Choose the path you'd like!"):
        question = prompt
        st.chat_message("user").markdown(question)

        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": question})