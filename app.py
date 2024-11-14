import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/799ce79f-29ea-43e7-9a67-8fabebd634a1"

def query_api(question):
    payload = {"question": question}
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again later."}
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to the API. Is it running?"}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot")

for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    elif msg['role'] == 'bot':
        st.markdown(f"**Bot:** {msg['content']}")

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    with st.spinner("Bot is typing..."):
        output = query_api(user_input)
    
    if 'error' in output:
        bot_response = "Sorry, I couldn't process your request."
        st.error(f"Error: {output['error']}")
    else:
        bot_response = output.get('answer', "I'm not sure how to respond to that.")
    
    st.session_state['messages'].append({"role": "bot", "content": bot_response})
    st.session_state['input'] = ""
    st.experimental_rerun()

if st.button("Clear Chat"):
    st.session_state['messages'] = []
    st.experimental_rerun()
