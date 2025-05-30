import os
import json
import streamlit as st
from openai import AzureOpenAI

# Load secrets from local.settings.json and set as environment variables
settings_path = os.path.join(os.path.dirname(__file__), "local.settings.json")
with open(settings_path, "r") as f:
    settings = json.load(f)

values = settings.get("Values", {})
for key, value in values.items():
    os.environ[key] = value

subscription_key = os.environ.get("AZURE_OPENAI_API_KEY")
endpoint = os.environ.get("ENDPOINT_URL")
deployment = os.environ.get("DEPLOYMENT_NAME", "gpt-4.1")
api_version = "2024-12-01-preview"

if not subscription_key:
    st.error("AZURE_OPENAI_API_KEY is not set in environment variables.")
else:
    st.info("AZURE_OPENAI_API_KEY loaded from environment variables.")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.title("Azure OpenAI Chatbot (env)")
st.markdown("""
This chatbot uses Azure OpenAI to answer your questions.\
Enter your prompt below and click **Ask** to get a response.
""")

col1, col2 = st.columns([1, 1])
with col1:
    clear = st.button("🧹 Clear Chat History")
if clear:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.experimental_rerun()

with st.form("chat_form"):
    user_input = st.text_area("Ask something:", "", height=80)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
    top_p = st.slider("Top-p (nucleus sampling)", 0.0, 1.0, 1.0, 0.01)
    max_tokens = st.number_input("Max tokens", min_value=1, max_value=2048, value=800)
    submitted = st.form_submit_button("Ask")

# Display chat history with avatars
st.markdown("### Chat History")
for msg in st.session_state.chat_history[1:]:  # skip system prompt
    if msg["role"] == "user":
        st.write(f"🧑 **You:** {msg['content']}")
    else:
        st.write(f"🤖 **Assistant:** {msg['content']}")

if submitted and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        try:
            client = AzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                api_key=subscription_key,
            )
            response = client.chat.completions.create(
                messages=st.session_state.chat_history,
                max_completion_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                model=deployment,
            )
            assistant_reply = response.choices[0].message.content
            st.session_state.chat_history.append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.success("Response:")
            st.write(f"🤖 **Assistant:** {assistant_reply}")
        except Exception as e:
            st.error(f"Error: {e}")
