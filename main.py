import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get and validate API key
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    st.error("API key not found. Please add it in the .env file.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Streamlit UI Enhancements
    st.set_page_config(page_title="AI Chatbot - Sohail Nawaz", page_icon="💬", layout="centered")
    st.title("💬 Gemini AI Chatbot - Sohail Nawaz")
    st.caption("Powered by Google's Gemini AI")
    
    # Styling
    st.markdown("""
        <style>
            .stChatInput input {border-radius: 10px; padding: 10px;}
            .stButton>button {background-color: #FF4B4B; color: white; border-radius: 10px;}
            .chat-message {margin-bottom: 10px; padding: 10px; border-radius: 8px;}
            .user-message {background-color: #1E88E5; color: white;}
            .assistant-message {background-color: #43A047; color: white;}
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
    
    # Display chat history with message numbers
    for i, message in enumerate(st.session_state.messages, 1):
        role_class = "user-message" if message["role"] == "user" else "assistant-message"
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="chat-message {role_class}"><strong>{i}. {message["role"].capitalize()}:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        with st.chat_message("user"):
            st.markdown(f'<div class="chat-message user-message"><strong>User:</strong> {prompt}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            with st.chat_message("assistant"):
                with st.spinner("💭 AI is thinking..."):
                    response = st.session_state.chat.send_message(prompt)
                    response_text = response.text
                    st.markdown(f'<div class="chat-message assistant-message"><strong>Gemini:</strong> {response_text}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

except Exception as e:
    st.error("Failed to initialize the chatbot. Please check your API key and connection.")
    st.stop()
