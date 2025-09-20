import streamlit as st
from Component.upload import render_uploader
from Component.chatUI import render_chat
from Component.history_download import render_history_download

st.set_page_config(page_title="AI Medical Chatbot", layout = "wide")
st.title("🩺 AI Medical Chatbot")

render_uploader()
render_chat()
render_history_download()