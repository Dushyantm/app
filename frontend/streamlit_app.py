# streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

def run_streamlit_app():
    st.title("AI Travel Agent")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to know about travel?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Send user input to API
        response = requests.post(f"{API_URL}/process_query", json={"text": prompt})
        
        if response.status_code == 200:
            data = response.json()
            if data["type"] == "database":
                assistant_response = f"Database Response: {data['results']['output']}"
            else:
                assistant_response = f"LLM Response: {data['response']}"
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            error_message = f"Error: {response.text}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    run_streamlit_app()