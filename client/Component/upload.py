import streamlit as st
from Utils.api import upload_pdfs_api, ask_question


def render_uploader():
  st.sidebar.header("Upload your medical PDFs")
  uploaded_files = st.sidebar.file_uploader("Upload multiple PDFs", type = "pdf", accept_multiple_files=True)
  if st.sidebar.button("Upload DB") and uploaded_files:
    response = upload_pdfs_api(uploaded_files)
    if response.status_code == 200:
      st.sidebar.success("Files uploaded successfully!")
    else:
      st.sidebar.error(f"Error: {response.text}")