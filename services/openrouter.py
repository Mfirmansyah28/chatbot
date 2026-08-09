from openai import OpenAI
import streamlit as st

MODEL_NAME = "nvidia/nemotron-3-nano-30b-a3b:free"

def get_client():
    """
    Membuat client OpenRouter.
    """
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )

def generate_response(messages, stream=True):
    """
    Mengirim pesan ke OpenRouter
    """
    client = get_client()
    return client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=stream,
    )