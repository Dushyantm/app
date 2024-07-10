import os
from backend import IntentDetection
from frontend import run_streamlit_app

def main():
    # response = IntentDetection(query).detect_intent()
    run_streamlit_app(IntentDetection)
    # return response

if __name__ == "__main__":
    # query = "What is the distance from London to New York?"
    # main(query=query)
    main()