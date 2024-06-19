import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",## Webpage name 
    page_icon=":brain:",  # Favicon emoji, The brain icon that shows near it
    layout="centered",  # Page layout option
)
st.header("ChatBot using Gemini-Pro") ##for giving the page a title

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") ## we have a variable named GOOGLE_API_KEY in the env file and that is what this function retrives

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY) ## configures the AI library with the api key
model = gen_ai.GenerativeModel('gemini-pro') ##intializes the model to gemini-pro
chat = model.start_chat(history=[]) ## starts a chat with an empty history
## Writing the code to get a response from the LLM
def get_response(question):
    response = chat.send_message(question,stream = True) ## sends the question to the LLM and streams the response back that is as the words come it gives it
    return response
## Intializing chat history if it doesnt exist
## session state holds all the variables of user interactions in the page
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [] ## if there is no chat_history we reset it to an empty list

input = st.text_input("Input",key = "input",placeholder="How can I help you today? ") ##creates a text input field for the user input and gives the input a key value 
submit = st.button("Ask the Question") ## Creates a button to ask the question
## to check that the button is pressed and the input is also not empty
if submit and input:
    response = get_response(input) ##uses the function to get a response from the model
    ## Add user query and the response to the chat history
    st.session_state["chat_history"].append(("You",input)) ##appends our question in the chat history as a pair of (role,question/input)
    st.subheader("The response is: ") ## Displays the subheader 
    ## for every chunk in the streamed response 
    for chunk in response:
        st.write(chunk.text) ## displaying the chunk
        st.session_state["chat_history"].append(("Bot",chunk.text)) ## adding the chunk to the chat_history
st.subheader("Chat History is: ") ##displays the subheader
## iterates over the chat history and prints the role with the text 
for role,text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")

    