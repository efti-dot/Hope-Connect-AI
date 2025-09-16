import streamlit as st
from prompt import OpenAIConfig

api_key = "api-key"
openai_config = OpenAIConfig(api_key=api_key)

def talk_with_AI():
    st.title("Hope AI")
    st.write("Feel free to ask anything about your need!")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("Ask about your need...", key="input")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        response = openai_config.get_response(user_input, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response)


def main():
    st.set_page_config(page_title="Hope AI", page_icon="🤖")
    talk_with_AI()


main()