import base64
import streamlit as st
import openai
import os

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("openai_api_key")

# Initialize the OpenAI client with the API key
openai.api_key = api_key

def get_answer(messages):
    system_message = [{"role": "system", "content": "You are a helpful AI chatbot that answers questions asked by User."}]
    messages = system_message + messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def text_to_speech(input_text):
    response = openai.Audio.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(f)
    return webm_file_path

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = openai.Audio.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How may I assist you today?"}]
