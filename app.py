import streamlit as st
import pandas as pd
from prompt import OpenAIConfig
from file_uploder import file_uploder

api_key = "api-key"
openai_config = OpenAIConfig(api_key=api_key)

def handle_file_upload():
    st.sidebar.title("Upload a File")
    uploaded_file = st.sidebar.file_uploader("Choose a file (CSV only)", type=["csv"])

    if uploaded_file:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
        df = pd.read_csv(uploaded_file)
        df_clean = file_uploder.preprocess_csv(df)
        st.session_state['csv_data'] = df_clean

def talk_with_AI():
    st.title("Hope AI 🤖")
    st.write("Feel free to ask anything about your need!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about your need...", key="input")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        context = None
        if 'csv_data' in st.session_state:
            df = st.session_state['csv_data']
            keywords = file_uploder.extract_keywords(user_input)
            filtered_df = file_uploder.filter_by_keywords(df, keywords)

            if not filtered_df.empty:
                chunks = file_uploder.chunk_dataframe(filtered_df)
                context = chunks[0]
                user_input = file_uploder.build_prompt(user_input, context, keywords)

        response = openai_config.get_response(user_input, st.session_state.messages)

        with st.chat_message("assistant"):
            st.markdown(response)

def main():
    st.set_page_config(page_title="Hope AI", page_icon="🤖")
    handle_file_upload()
    talk_with_AI()

main()