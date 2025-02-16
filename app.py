import streamlit as st
import requests
import uuid

API_URL = "http://localhost:3000/api/v1/prediction/6522dbdf-e7df-47f4-a206-d48a022cf632"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

st.title("Chatbot Streamlit App")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = str(uuid.uuid4())
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'chat_message_id' not in st.session_state:
    st.session_state['chat_message_id'] = None  # Will be set when sending a message

# Display the conversation using st.chat_message
for message in st.session_state['messages']:
    role = message['role'].lower()
    if role == 'user':
        with st.chat_message("user"):
            st.write(message['content'])
    else:
        with st.chat_message("assistant"):
            st.write(message['content'])

# Accept user input using st.chat_input
user_input = st.chat_input("Type your message here...")

if user_input:
    user_input = user_input.strip()
    if user_input:
        # Generate a new chat_message_id for each user message
        st.session_state['chat_message_id'] = str(uuid.uuid4())

        # Append user message to session state and display it
        st.session_state['messages'].append({'role': 'user', 'content': user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Prepare payload for API request
        payload = {
            "question": user_input,
            "chatId": st.session_state['chat_id'],
            "sessionId": st.session_state['session_id'],
            "chatMessageId": st.session_state['chat_message_id'],
        }

        # Send the request and get the response
        try:
            data = query(payload)
            bot_reply = data.get('text', 'No response from the bot.')

            # Append bot reply to session state and display it
            st.session_state['messages'].append({'role': 'assistant', 'content': bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before sending.")
