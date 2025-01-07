import streamlit as st
import json
import random
from datetime import datetime
from difflib import SequenceMatcher

# Load the JSON file containing prompt-response pairs
with open("usecase1.json", "r") as file:
    prompt_data = json.load(file)

# Function to find the best matching response for a user query
def find_best_response(prompt):
    best_match = None
    best_score = 0.0

    for pair in prompt_data:
        stored_prompt = pair["prompt"]
        score = SequenceMatcher(None, prompt.lower(), stored_prompt.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = pair["completion"]

    if best_score > 0.5:  # Adjust the threshold as needed
        return best_match
    else:
        return "Sorry, I could not find a suitable response for your query."

# Set Streamlit page configuration
st.set_page_config(page_title=" Chatbot", layout="wide")

# Initialize session state for chat , query, and prompts
if "history" not in st.session_state:
    st.session_state["history"] = []  # Stores the chat history as a list of dicts
if "query" not in st.session_state:
    st.session_state["query"] = ""  # Stores the current query
if "prompts" not in st.session_state:
    st.session_state["prompts"] = random.sample(prompt_data, 4)  # Generate random prompts

# CSS for chat bubbles
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        margin: 10px;
        border-radius: 20px;
        max-width: 70%;
        line-height: 1.5;
    }
    .user {
        background-color: #d1e7dd;
        color: #0f5132;
        text-align: right;
        align-self: flex-end;
    }
    .bot {
        background-color: #f8d7da;
        color: #842029;
        text-align: left;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# UI Header
st.markdown(
    """
    <div style="text-align: center; padding: 20px; color: black; border-radius: 10px;">
        <h1 style="font-family: Arial, sans-serif; font-size: 2.5em; margin: 0;">🤖 Chatbot</h1>
        <p style="font-size: 1.2em; margin: 10px 0;">Ask me anything about Outlook troubleshooting </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat History Section
st.subheader("💬 Chat ")
if st.session_state["history"]:
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state["history"]:
            timestamp = datetime.strptime(chat["timestamp"], "%H:%M:%S")  # Parse the timestamp
            formatted_time = timestamp.strftime("%I:%M %p")  # Convert to standard format
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="chat-bubble user">🧑‍💻: {chat['user']} <br><sub>_{formatted_time}_</sub></div>
                    <div class="chat-bubble bot">🤖 : {chat['bot']} <br><sub>_{formatted_time}_</sub></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("No conversation history yet.")

if st.button("Clear Chat "):
    st.session_state["history"].clear()
    st.info("Chat cleared!")


# Query Input Section
st.subheader("📝 Enter Your Query")
# Randomized "Try prompts"
cols = st.columns(2)
for i, prompt in enumerate(st.session_state["prompts"]):
    with cols[i % 2]:
        if st.button(prompt["prompt"], key=f"prompt-{i}"):
            st.session_state["query"] = prompt["prompt"]  # Update the query box with the selected prompt
query_input = st.text_input(
    "Type your query below:",
    value=st.session_state["query"],
    placeholder="Enter your message here..."
)


# Submit Query Button
if st.button("Submit Query"):
    if query_input.strip():  # Check if the input is not empty or only spaces
        st.session_state["query"] = query_input  # Update the query in session state
        bot_response = find_best_response(st.session_state["query"])
        st.session_state["history"].append({
            "user": st.session_state["query"],
            "bot": bot_response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.session_state["query"] = ""  # Clear input after submission
    else:
        st.warning("Please enter a query.")









