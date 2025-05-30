import os
import json
import streamlit as st
from openai import AzureOpenAI

# Load secrets from local.settings.json
settings_path = os.path.join(os.path.dirname(__file__), "local.settings.json")
with open(settings_path, "r") as f:
    settings = json.load(f)

values = settings.get("Values", {})
subscription_key = values.get("AZURE_OPENAI_API_KEY")
endpoint = values.get("ENDPOINT_URL")
deployment = values.get("DEPLOYMENT_NAME", "gpt-4.1")
api_version = "2024-12-01-preview"

# Debug print to check if environment variables are loaded
if not subscription_key:
    st.error("AZURE_OPENAI_API_KEY is not set in local.settings.json.")
else:
    st.info("AZURE_OPENAI_API_KEY loaded from local.settings.json.")

st.title("Azure OpenAI Chatbot")
user_input = st.text_input("Ask something:", "I am going to Paris, what should I see?")

if st.button("Ask"):
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        max_completion_tokens=800,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment,
    )
    st.write(response.choices[0].message.content)
