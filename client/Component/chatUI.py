import streamlit as st
from Utils.api import upload_pdfs_api, ask_question


def render_chat():
  st.subheader("Chat with your assistant")

  if "messages" not in st.session_state:  # Initialize chat history
    st.session_state.messages = []

  #render chat messages from history on app 
  for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])
    
  #input and respond to user message
  user_input = st.chat_input("Type your question here...")
  if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    response = ask_question(user_input)
    if response.status_code == 200:
      data = response.json()
      answer = data["response"]
      sources = data.get("sources", [])
      st.chat_message("assistant").markdown(answer)
      if sources:
        st.markdown("📃 **Sources:**")
        for src in sources:
          st.markdown(f"- {src}")

      st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
      st.error(f"Error : {response.text}")
  