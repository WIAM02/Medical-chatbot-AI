from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA #Connects a retriever and an LLM to answer questions using retrieved documents.
from langchain_groq import ChatGroq #Lets you use Groq-hosted LLMs (fast, low-latency) inside LangChain.
import os
from dotenv import load_dotenv

#LangChain = a framework that makes it easy to connect LLMs with your data, tools, and workflows.
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
  llm = ChatGroq(
    groq_api_key= GROQ_API_KEY,
    model_name = 'llama-3.3-70b-versatile'
  )
  
  prompt = PromptTemplate(
    input_variables =["context", "question"],
    template = """ 
    You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

    Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

    ---

    🔍 **Context**:
    {context}

    🙋‍♂️ **User Question**:
    {question}

    ---

    💬 **Answer**:
    - Respond in a calm, factual, and respectful tone.
    - Use simple explanations when needed.
    - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
    - Do NOT make up facts.
    - Do NOT give medical advice or diagnoses.
        """
      )
  return RetrievalQA.from_chain_type(
    llm = llm,
    chain_type = "stuff",
    retriever = retriever,
    chain_type_kwargs ={"prompt": prompt},
    return_source_documents = True,
  )
  
# This function creates a custom RAG pipeline that:

# Uses Groq’s LLaMA-3 model

# Retrieves relevant documents via the provided retriever

# Passes them into a carefully crafted medical-aware prompt

# Returns both the model’s answer and the source documents