import streamlit as st
import pandas as pd
from prompt import OpenAIConfig
from file_uploder import file_uploder

api_key = "api-key"
openai_config = OpenAIConfig(api_key=api_key)

def handle_file_upload():
    st.sidebar.title("Upload a File")
    uploaded_file = st.sidebar.file_uploader("Choose a file (CSV only)", type=["csv"])

    # Location selector
    st.sidebar.markdown("### Select Your Location")
    locations = [
        "11111 W Flamingo Rd, Las Vegas, NV 89135",
        "525 E Bonanza Rd, Las Vegas, NV 89101",
        "2000 S Maryland Pkwy, Las Vegas, NV 89104",
        "Custom location"
    ]
    selected_location = st.sidebar.selectbox("Choose a location", locations)

    if selected_location == "Custom location":
        custom_location = st.sidebar.text_input("Enter your location")
        if custom_location:
            st.session_state['user_location'] = custom_location
    else:
        st.session_state['user_location'] = selected_location

    # CSV upload
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
        keywords = []

        if 'csv_data' in st.session_state:
            df = st.session_state['csv_data']
            keywords = file_uploder.extract_keywords(user_input)
            filtered_df = file_uploder.filter_by_keywords(df, keywords)

            if not filtered_df.empty:
                chunks = file_uploder.chunk_dataframe(filtered_df)
                context = chunks[0]

        location = st.session_state.get('user_location', '')
        if location:
            user_input += f"\n\nMy current location is: {location}"
        prompt = user_input

        response = openai_config.get_response(prompt, st.session_state.messages, context=context if context else "")


        with st.chat_message("assistant"):
            st.markdown(response)


def main():
    st.set_page_config(page_title="Hope AI", page_icon="🤖")
    handle_file_upload()
    talk_with_AI()

main()