# streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

def run_streamlit_app():
    st.title("AI Travel Agent")

    user_input = st.text_input("Ask me anything about travel:", "")
    
    if st.button("Submit"):
        if user_input:
            response = requests.post(f"{API_URL}/process_query", json={"text": user_input})
            if response.status_code == 200:
                data = response.json()
                if data["type"] == "database":
                    st.write("Quering the database...")
                    st.write("Database Response:", data["results"]['output'])
                else:
                    st.write("LLM Response:", data["response"])
            else:
                st.write("Error:", response.text)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    run_streamlit_app()