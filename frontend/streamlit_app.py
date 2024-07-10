import streamlit as st

def run_streamlit_app(process_query_func):
    st.title("AI Travel Agent")

    user_input = st.text_input("Ask me anything about travel:", "")
    
    if st.button("Submit"):
        if user_input:
            response = process_query_func(user_input).detect_intent()
            st.write("Response:", response)
        else:
            st.write("Please enter a query.")