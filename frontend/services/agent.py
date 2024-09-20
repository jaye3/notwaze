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
            "content": "Hello! I got all the info you just entered! How do you want to personalize your route?"
        }]

    # Initialize session id
    if 'sessionId' not in st.session_state:
        st.session_state['sessionId'] = ""

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate route when chatbot initializes
    url = "http://ec2-100-26-41-70.compute-1.amazonaws.com:80/generate_route"  

    try:
        response = requests.post(url)  # Call the endpoint without parameters
        route_response = response.json()  # Parse the JSON response

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
    if prompt := st.chat_input("What is up?"):
        question = prompt
        st.chat_message("user").markdown(question)

        # Here you can implement additional logic for other user interactions if needed
        # For example, you can call another endpoint or process the user's question

        # Example placeholder response
        st.chat_message("assistant").markdown("I'm here to assist you with your questions!")

        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": question})