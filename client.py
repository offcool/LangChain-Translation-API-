import requests
import streamlit as st

def get_groq_response(input_text):
    # Construct the JSON body
    json_body = {
        "text": input_text,  # The text to be translated
        "language": "Russian"  # Language to translate to
    }
    
    try:
        # Send a POST request with the JSON body
        response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract the 'result' from the JSON response
        result = response.json().get("result", "")
        return result  # Return only the result text
    except requests.ConnectionError as e:
        return f"Connection error: {e}"
    except requests.HTTPError as e:
        return f"HTTP error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app
st.title("LLM Application using LCEL __ version 1.0")
input_text = st.text_input("Enter the text you want to convert to Russian")

if input_text:
    # Get the result from the function and display it
    translated_text = get_groq_response(input_text)
    st.write(translated_text)  # Display only the result text

