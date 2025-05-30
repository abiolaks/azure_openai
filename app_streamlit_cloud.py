import streamlit as st
from openai import AzureOpenAI

subscription_key = st.secrets["AZURE_OPENAI_API_KEY"]
endpoint = st.secrets["ENDPOINT_URL"]
deployment = st.secrets.get("DEPLOYMENT_NAME", "gpt-4.1")
api_version = "2024-12-01-preview"

if not subscription_key:
    st.error("AZURE_OPENAI_API_KEY is not set in Streamlit secrets.")
else:
    st.info("AZURE_OPENAI_API_KEY loaded from Streamlit secrets.")

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
