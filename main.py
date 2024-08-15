import asyncio
import streamlit as st
import threading
from nemoguardrails import LLMRails, RailsConfig

st.title('Storyspire AI')


config = RailsConfig.from_path("./config")

try:
    loop = asyncio.get_event_loop()
except RuntimeError as e:
    if str(e) == 'There is no current event loop in thread %r.' % threading.current_thread().name:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

rails = LLMRails(config)

def get_response(prompt):
    completion = rails.generate(messages=[
        # {"role": "system", "content": "When you write stories, you respond with the story verbatim including no other conversational text."},
        {"role": "user", "content": prompt}])
    return completion['content']

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({"role": "USER", "message": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            message_placeholder = st.empty()
            full_response = get_response(prompt)
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "CHATBOT", "message": full_response})

