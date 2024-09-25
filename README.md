# WalkEaze
Using Singapore's proprietary mapping service, WalkEaze aims to empower the public to personalise their health goals in even the smallest of actions through their walking routes.

This project was created for the Singapore Land Authority-Amazon Web Services Geospatial Innovation Challenge. Our team tackled the challenge statement, "Using OneMap to suggest a walking trail based on one’s health goals". 

## Demo video
TBC

# Installation/Running the localhost

If you would like to locally download the repo, we recommend setting up a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
Install the necessary dependencies with:
<br>
```pip install -r requirements. txt```

To run on localhost, navigate into the **app** folder and use this command in the terminal:
<br>
```streamlit run app.py```
<br>
This will open up a new tab in your browser. To close the session, use <kbd>Ctrl</kbd> + <kbd>C</kbd> in the same terminal. 
<br>
<i> *You may need to do this twice to ensure the session has closed.</i>

## About the project

This web app is intended as a Proof-of-Concept in integrating OneMap APIs and Generative AI in the use case of walking goals. 
As usage of the OneMap APIs and AWS provided were criteria for the product, we mainly used these resources to build our POC. 
<br>
For the purposes of the proof-of-concept and with this being our main foray into full-stack development, we chose to use Streamlit-FastAPI for our tech stack.
<br><br>
During development, we faced numerous challenges such as handling of geojson data, formulating an algorithm that worked around the pros and cons of the OneMap routing API, andthe compatibility in integration between the frontend and backend. 
<br><br>
Other future considerations include:
<br>--> native mobile development 
<br>--> better conversion of parks as POIs
<br>--> adding more amenity types (e.g. water drinking points) to routes/routing considerations
<br>--> Deploying onto a different tech stack for more reliability and scaleability (e.g. Next.js/Vercel)

## Technologies used
 - AWS Bedrock
 - OneMap APIs
 - Streamlit (for hosting the web app)
 - [Link to the backend repo, hosted on EC2 with Docker](https://github.com/drgnfrts/notwaze-backend)

# Credits
Created by Heng Kuan Xin, Jay Choa, Nicolas Tang, and Zara Mufti

Sending appreciation to these fellas for the help and inspiration:
- Prof. Kam Tin Seong, for his guidance and advice
- SLA Team, for organising this competition
- [Contextual Chatbots using AWS Bedrock - Streamlit](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/rag-solutions/contextual-chatbot-using-knowledgebase)
- [Streamlit JS Eval for geolocation](https://github.com/aghasemi/streamlit_js_eval)
- [Keyup for live searchbar](https://github.com/blackary/streamlit-keyup)
- [ST Folium for integrating the map render](https://github.com/randyzwitch/streamlit-folium/tree/master)