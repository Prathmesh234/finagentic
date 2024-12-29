import streamlit as st
from datetime import datetime
import asyncio
from Orchestrator import main  # Import the function from Orchestrator.py

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar for conversation history
st.sidebar.title("Conversation History")
if st.session_state["messages"]:
    for i, msg in enumerate(st.session_state["messages"]):
        if msg["role"] == "user":
            st.sidebar.write(f"User: {msg['content']}")
        else:
            st.sidebar.write(f"Bot: {msg['content']}")
        st.sidebar.write(f"Time: {msg['timestamp']}")
        st.sidebar.write("---")

# Title
st.title("ChatGPT-like Interface")

# Input container
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Your message", placeholder="Type your message here...")
    send_button = st.form_submit_button("Send")

# Handle user input
if send_button and user_input:
    # User message is passed here
    st.session_state["messages"].append({"role": "user", "content": user_input, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    
    # Execute Orchestrator.py to get the agent's response
    response = asyncio.run(main(user_input))  # Call the function from Orchestrator.py
    
    # Agent reply is added here
    if response:
        st.session_state["messages"].append({"role": "agent", "content": response, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.write(f"User: {msg['content']} ({msg['timestamp']})")
    else:
        st.write(f"Bot: {msg['content']} ({msg['timestamp']})")