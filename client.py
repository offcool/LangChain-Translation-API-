import requests
import streamlit as st
import os

def get_groq_response(input_text):
    # Construct the JSON body
    json_body = {
        "text": input_text,  # The text to be translated
        "language": "French"  # Language to translate to
    }
    
    try:
        # Send a POST request with the JSON body
        response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
        response.raise_for_status()  
        
        # Extract the 'result' from the JSON response
        result = response.json().get("result", "")
        return result  # Return only the result text
    except requests.ConnectionError as e:
        return f"Connection error: {e}"
    except requests.HTTPError as e:
        return f"HTTP error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Language Translation App", page_icon="favicon.png")

col1, col2 = st.columns([1, 5])  

with col1:
    st.image("favicon.png", width=80)  

with col2:
    st.title("Langchain Language Translation App using LCEL (Version 1.0)")
    st.write("### Enter text to translate it into French:")

input_text = st.text_input("Text to Translate", "")

if st.button("Translate"):
    if not input_text:
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            translated_text = get_groq_response(input_text)
            st.success("Translation successful!")
            st.write("### Translated Text:")
            st.write(translated_text)  

st.markdown("---")
st.write("#### About this App")
st.write("This application utilizes a FastAPI backend to translate text into French using advanced language models.")
st.write("For more information, visit the [GitHub Repository](#).")  # Replace with actual URL if available

st.markdown("---")
st.markdown("© 2024 SHERPA Engineering MENA. All rights reserved.")
