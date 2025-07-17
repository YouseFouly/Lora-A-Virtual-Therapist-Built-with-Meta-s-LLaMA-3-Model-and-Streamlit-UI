import os
import json
import streamlit as st
from openai import OpenAI
import requests
from streamlit_lottie import st_lottie

# -------------------- Load Lottie Animation --------------------
def load_lottie_url(url: str):
    response = requests.get(url)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Failed to parse JSON from URL.")
        print("Response content:", response.text[:200])
        return None

lottie_json = load_lottie_url("https://lottie.host/cc13fe2f-25c4-4547-b89a-5059f4044de4/Gn62lcFzBl.json")

# -------------------- Load API Key --------------------
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")
config_data = json.load(open(config_path))
OPENROUTER_API_KEY = config_data["OPENROUTER_API_KEY"]

# -------------------- Initialize OpenRouter Client --------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# -------------------- Page Config (Centered Layout) --------------------
st.set_page_config(
    page_title="TherapAI",
    page_icon="🧠",
    layout="centered"  # ✅ Centered layout like before
)

# -------------------- Chat UI --------------------
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page title
st.markdown(
    """
    <div style='text-align: center;'>
        <h3>Hello! I’m Lora — your Virtual Therapist, here for you 🫂</h3>
    </div>
    """,
    unsafe_allow_html=True
)



# Display Lottie animation (optional, below title)
if lottie_json:
    st_lottie(lottie_json, speed=1, loop=True, height=300)
else:
    st.error("❌ Failed to load animation.")

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input bar at the bottom (automatically pinned)
user_prompt = st.chat_input("Take a deep breath and feel free to share....")
if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        # Get assistant response
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[
                {"role": "system", "content": "You are a supportive and empathetic therapist. Help the user feel heard and safe. Your name is Lora. make your answers short and up to the point"},
                *st.session_state.chat_history
            ]
        )
        assistant_response = response.choices[0].message.content

        # Display assistant reply
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"❌ Error: {e}")
