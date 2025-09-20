from pydantic import Field
from re import match
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_hundlers import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import os
from pydantic import BaseModel
from logger import logger
from typing import List , Optional

router = APIRouter()

@router.post("/ask/")
async def ask_question(question:str = Form(...)):   #runs without blocking other requests
  try:
    logger.info("User query: %s", question)
    
     #embeddings and vectorstore setup
    pc = Pinecone(api_key= os.environ["PINECONE_API_KEY"])
    index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
    embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
    embedded_query = embed_model.embed_query(question) #qst embedded
    res = index.query(vector = embedded_query, top_k=3, include_metadata=True)  # top_k=3 → return the 3 most similar results.
    
    docs=[
      Document(
        page_content=m ['metadata'].get('text', ''),
        metadata= m ['metadata']
      ) for m  in res['matches']
    ]
    print(f"Display {docs}")
    #exempl 
    #     res['matches'] = [
    #     {
    #         "id": "doc1",
    #         "score": 0.89,
    #         "metadata": {"text": "This is some content", "source": "file1.txt"}
    #     },
    #     {
    #         "id": "doc2",
    #         "score": 0.82,
    #         "metadata": {"text": "Another piece of content", "source": "file2.txt"}
    #     }
    # ]

    
    class SimpleRetriever(BaseRetriever):
      docs: List[Document]
      
      def _get_relevant_documents(self, query:str) -> List[Document]:
        return self.docs
      # This class is a custom retriever that extends LangChain’s BaseRetriever. 
      # A retriever’s job in LangChain is to fetch documents that are relevant to a given query.

    retriever = SimpleRetriever(docs = docs)
    print(f"Retrieved {retriever}")     # we ask qst -> retriever looks through all doc -> returns relevant doc to llm chain
    chain = get_llm_chain(retriever)
    result = query_chain(chain, question)

    logger.info("Generated response: %s", result)
    return result
    
  except Exception as e:
    logger.exception("Error during question processing")
    return JSONResponse(status_code=500, content={"error": str(e)})