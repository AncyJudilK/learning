# import streamlit as st
# import json
# import random
# from datetime import datetime
# from difflib import SequenceMatcher
 
# # Load the JSON file containing prompt-response pairs
# with open("usecase1.json", "r") as file:
#     prompt_data = json.load(file)
 
# # Function to find the best matching response for a user query
# def find_best_response(prompt):
#     best_match = None
#     best_score = 0.0
 
#     for pair in prompt_data:
#         stored_prompt = pair["prompt"]
#         score = SequenceMatcher(None, prompt.lower(), stored_prompt.lower()).ratio()
#         if score > best_score:
#             best_score = score
#             best_match = pair["completion"]
 
#     if best_score > 0.5:  # Adjust the threshold as needed
#         return best_match
#     else:
#         return "Sorry, I could not find a suitable response for your query."
 
# # Set Streamlit page configuration
# st.set_page_config(page_title="Chatbot", layout="wide")
 
# # Define target keywords
# keywords = [
#     "outlook freezes", "outlook indexing", "outlook rebuild",
#     "outlook search", "password", "password reset",
#     "password expiry", "account lockout", "disabled accounts",
#     "terminated accounts", "lockout policy", "password policy"
# ]
 
# # Initialize session state for chat, query, prompts, and keyword tracking
# if "history" not in st.session_state:
#     st.session_state["history"] = []  # Stores the chat history as a list of dicts
# if "query" not in st.session_state:
#     st.session_state["query"] = ""  # Stores the current query
# if "keyword_counts" not in st.session_state:
#     st.session_state["keyword_counts"] = {keyword: 0 for keyword in keywords}  # Track keyword search counts
 
# # CSS for chat bubbles and related question styling
# st.markdown(
#     """
#     <style>
#     .chat-bubble {
#         padding: 10px 15px;
#         margin: 10px;
#         border-radius: 20px;
#         max-width: 70%;
#         line-height: 1.5;
#     }
#     .user {
#         background-color: #d1e7dd;
#         color: #0f5132;
#         text-align: right;
#         align-self: flex-end;
#     }
#     .bot {
#         background-color: #f8d7da;
#         color: #842029;
#         text-align: left;
#         align-self: flex-start;
#     }
#     .related-questions {
#         margin: 20px 0;
#     }
#     .related-question {
#         padding: 10px;
#         margin: 5px;
#         background-color: #f1f1f1;
#         border: 1px solid #ddd;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     .related-question:hover {
#         background-color: #e3e3e3;
#     }
#     .keyword-box {
#         background-color: transparent;  /* Make the background invisible */
#         border: none;  /* Remove the border */
#         padding: 5px;  /* Adjust padding for compactness */
#         margin-left: 10px;  /* Add space between the box and the button */
#         font-size: 1em;  /* Slightly smaller font size */
#         color: #333;  /* Dark text for visibility */
#         display: inline-block;  /* Align it inline with the button */
#         vertical-align: middle;  /* Align vertically with the button */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
 
# # UI Header
# st.markdown(
#     """
#     <div style="text-align: center; padding: 20px; color: black; border-radius: 10px;">
#         <h1 style="font-family: Arial, sans-serif; font-size: 2.5em; margin: 0;">🤖 Chatbot</h1>
#         <p style="font-size: 1.2em; margin: 10px 0;">Ask me anything about Outlook troubleshooting </p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

 
# # Chat History Section
# st.subheader("💬 Chat")
# if st.session_state["history"]:
#     for chat in st.session_state["history"]:
#         timestamp = datetime.strptime(chat["timestamp"], "%H:%M:%S")
#         formatted_time = timestamp.strftime("%I:%M %p")
#         st.markdown(
#             f"""
#             <div class="chat-container">
#                 <div class="chat-bubble user">🧑‍💻: {chat['user']} <br><sub>_{formatted_time}_</sub></div>
#                 <div class="chat-bubble bot">🤖 : {chat['bot']} <br><sub>_{formatted_time}_</sub></div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
# else:
#     st.info("No conversation history yet.")
 
# if st.button("Clear Chat"):
#     st.session_state["history"].clear()
#     st.info("Chat cleared!")
 
# # Query Input Section
# st.subheader("📝 Enter Your Query")
# query_input = st.text_input("Type your question:", value=st.session_state["query"], key="query_input")
 
 
 
 
# # Show related questions if the query contains any keywords
# if query_input.strip():  # Ensure query_input is not empty
#     # Identify keywords present in the query
#     matching_keywords = [keyword for keyword in keywords if keyword in query_input.lower()]
   
#     # Update the keyword count for each matching keyword
#     for keyword in matching_keywords:
#         st.session_state["keyword_counts"][keyword] += 1
   
#     # Fetch related questions for the matching keywords
#     related_questions = [
#         pair["prompt"] for pair in prompt_data
#         if any(keyword in pair["prompt"].lower() for keyword in matching_keywords)
#     ]
   
#     # Display related questions
#     if related_questions:
#         st.markdown("### Related Questions")
#         for question in related_questions[:4]:  # Show only the first 4 related questions
#             if st.button(question, key=question):
#                 st.session_state["query"] = question  # Update query
#                 query_input = question
 
 
# # Submit Query Button with Most Searched Keyword Display
# col1, col2 = st.columns([2, 1])  # Create two columns for better layout
# with col1:
#     if st.button("Submit Query"):
#         if query_input.strip():  # Check if the input is not empty or only spaces
#             st.session_state["query"] = query_input  # Update the query in session state
#             bot_response = find_best_response(st.session_state["query"])
#             st.session_state["history"].append({
#                 "user": st.session_state["query"],
#                 "bot": bot_response,
#                 "timestamp": datetime.now().strftime("%H:%M:%S")
#             })
#             st.session_state["query"] = ""  # Clear input after submission
#         else:
#             st.warning("Please enter a query.")
 
# with col2:
#     sorted_keywords = sorted(st.session_state["keyword_counts"].items(), key=lambda x: x[1], reverse=True)
#     most_searched_keyword = sorted_keywords[0] if sorted_keywords else ("None", 0)
#     st.markdown(
#         f"""
#         <div class="keyword-box">
#             <italic>Most Searched Keyword: </italic>
#             {most_searched_keyword[0]}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )




# import streamlit as st
# import json
# from datetime import datetime
# from difflib import SequenceMatcher

# # Load the JSON file containing prompt-response pairs
# with open("usecase1.json", "r") as file:
#     prompt_data = json.load(file)

# # Function to find the best matching response for a user query
# def find_best_response(prompt):
#     best_match = None
#     best_score = 0.0

#     for pair in prompt_data:
#         stored_prompt = pair["prompt"]
#         score = SequenceMatcher(None, prompt.lower(), stored_prompt.lower()).ratio()
#         if score > best_score:
#             best_score = score
#             best_match = pair["completion"]

#     if best_score > 0.5:  # Adjust the threshold as needed
#         return best_match
#     else:
#         return "Sorry, I could not find a suitable response for your query."

# # Set Streamlit page configuration
# st.set_page_config(page_title="Chatbot", layout="wide")

# # Initialize session state for chat, query, and prompts
# if "history" not in st.session_state:
#     st.session_state["history"] = []  # Stores the chat history as a list of dicts
# if "query" not in st.session_state:
#     st.session_state["query"] = ""  # Stores the current query

# # CSS for chat bubbles and related question styling
# st.markdown(
#     """
#     <style>
#     .chat-bubble {
#         padding: 10px 15px;
#         margin: 10px;
#         border-radius: 20px;
#         max-width: 70%;
#         line-height: 1.5;
#     }
#     .user {
#         background-color: #d1e7dd;
#         color: #0f5132;
#         text-align: right;
#         align-self: flex-end;
#     }
#     .bot {
#         background-color: #f8d7da;
#         color: #842029;
#         text-align: left;
#         align-self: flex-start;
#     }
#     .chat-container {
#         display: flex;
#         flex-direction: column;
#         align-items: flex-start;
#         margin-bottom: 20px;
#     }
#     .chat-container .user {
#         align-self: flex-end;
#     }
#     .chat-header {
#         text-align: center;
#         padding: 20px;
#         color: black;
#         border-radius: 10px;
#     }
#     .chat-header h1 {
#         font-family: Arial, sans-serif;
#         font-size: 2.5em;
#         margin: 0;
#     }
#     .chat-header p {
#         font-size: 1.2em;
#         margin: 10px 0;
#     }
#     .submit-container {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-top: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # UI Header
# st.markdown(
#     """
#     <div class="chat-header">
#         <h1>🤖 Chatbot</h1>
#         <p>Ask me anything about Outlook troubleshooting</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # Chat History Section
# st.subheader("💬 Chat")
# if st.session_state["history"]:
#     for chat in st.session_state["history"]:
#         timestamp = datetime.strptime(chat["timestamp"], "%H:%M:%S")
#         formatted_time = timestamp.strftime("%I:%M %p")
#         st.markdown(
#             f"""
#             <div class="chat-container">
#                 <div class="chat-bubble user">🧑‍💻: {chat['user']} <br><sub>_{formatted_time}_</sub></div>
#                 <div class="chat-bubble bot">🤖: {chat['bot']} <br><sub>_{formatted_time}_</sub></div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
# else:
#     st.info("No conversation history yet.")

# if st.button("Clear Chat"):
#     st.session_state["history"].clear()
#     st.info("Chat cleared!")

# # Query Input Section
# st.subheader("📝 Enter Your Query")
# query_input = st.text_input("Type your question:", value=st.session_state["query"], key="query_input")

# # Submit Query Button
# if st.button("Submit Query"):
#     if query_input.strip():  # Check if the input is not empty or only spaces
#         st.session_state["query"] = query_input  # Update the query in session state
#         bot_response = find_best_response(st.session_state["query"])
#         st.session_state["history"].append({
#             "user": st.session_state["query"],
#             "bot": bot_response,
#             "timestamp": datetime.now().strftime("%H:%M:%S")
#         })
#         st.session_state["query"] = ""  # Clear input after submission
#     else:
#         st.warning("Please enter a query.")





import streamlit as st
import json
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
st.set_page_config(page_title="Query Portal", layout="wide")

# Initialize session state for chat, query, and prompts
if "history" not in st.session_state:
    st.session_state["history"] = []  # Stores the chat history as a list of dicts
if "query" not in st.session_state:
    st.session_state["query"] = ""  # Stores the current query

# CSS for styling chat bubbles, buttons, and the query interface
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
        align-items: flex-start;
        margin-bottom: 20px;
    }
    .chat-container .user {
        align-self: flex-end;
    }
    .chat-header {
        text-align: center;
        padding: 20px;
        color: black;
        border-radius: 10px;
    }
    .chat-header h1 {
        font-family: Arial, sans-serif;
        font-size: 2.5em;
        margin: 0;
    }
    .chat-header p {
        font-size: 1.2em;
        margin: 10px 0;
    }
    .submit-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# UI Header
st.markdown(
    """
    <div class="chat-header">
        <h1>🤖 Chatbot</h1>
        <p>Ask me anything about Outlook troubleshooting</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Predefined Query Section
st.subheader("📝 Enter Your Query")
col1, col2 = st.columns(2)

with col1:
    if st.button("How many invalid login attempts will lock an account in Verint?"):
        st.session_state["history"].append({
            "user": "How many invalid login attempts will lock an account in Verint?",
            "bot": "The account will be locked after 5 invalid login attempts.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    if st.button("Will GSD change passwords or enable disabled accounts?"):
        st.session_state["history"].append({
            "user": "Will GSD change passwords or enable disabled accounts?",
            "bot": "Yes, GSD can change passwords and enable disabled accounts based on authorization.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

with col2:
    if st.button("How to check the indexing status in Microsoft Outlook?"):
        st.session_state["history"].append({
            "user": "How to check the indexing status in Microsoft Outlook?",
            "bot": "To check the indexing status, go to Outlook Options -> Search -> Indexing Options.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    if st.button("Can GSD unlock any account locked in Active Directory?"):
        st.session_state["history"].append({
            "user": "Can GSD unlock any account locked in Active Directory?",
            "bot": "Yes, GSD can unlock accounts in Active Directory with the proper authorization.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

# Custom Query Input Section
query_input = st.text_input("Type your query below:", value=st.session_state["query"], key="query_input")

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
        st.warning("Please enter a query before submitting.")

# Chat History Section
st.subheader("💬 Chat History")
if st.session_state["history"]:
    for chat in st.session_state["history"]:
        timestamp = datetime.strptime(chat["timestamp"], "%H:%M:%S")
        formatted_time = timestamp.strftime("%I:%M %p")
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="chat-bubble user">🧑‍💻: {chat['user']} <br><sub>_{formatted_time}_</sub></div>
                <div class="chat-bubble bot">🤖: {chat['bot']} <br><sub>_{formatted_time}_</sub></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("No conversation history yet.")

if st.button("Clear Chat"):
    st.session_state["history"].clear()
    st.info("Chat cleared!")


