import os 
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import streamlit as st
from PyPDF2 import PdfReader
import tensorflow as tf
import torch
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from tenacity import retry, wait_exponential, stop_after_attempt
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import sqlite3
#from langchain.vectorstores import FAISS



import warnings
torch.cuda.empty_cache()

warnings.filterwarnings("ignore", category=FutureWarning)

os.environ["HF_TOKEN"]='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'
api_key="jbd91deBY9trpxPN0PXwbvv9wRVimiaU"

#api_key = os.getenv("MISTRAL_API_KEY")



#
def rag_pdf(pdf):
    pdf = PdfReader(pdf)

    # Saving the entire pdf as a raw_text
    from typing_extensions import Concatenate

    raw_text = ' '
    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
            raw_text +=content
    text_splitter = RecursiveCharacterTextSplitter()

    # Converting the Data into Chunks
    documents = text_splitter.split_text(raw_text)

    # Convert the list of strings to a list of Document objects
    documents = [Document(page_content=text) for text in documents]
   

    local_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")


    vector = FAISS.from_documents(documents, local_embeddings)

    # Define a retriever interface
    retriever = vector.as_retriever()
    
    # Define LLM
    model = ChatMistralAI(mistral_api_key=api_key)
    # Define prompt template
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    # Create a retrieval chain to answer questions
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain


def answer_generator(retrieval_chain,query):
    # Retry mechanism with exponential backoff
    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
    def invoke_with_retry(chain, input_data):
        return chain.invoke(input_data)



    response = invoke_with_retry(retrieval_chain, {"input": query})
    st.write(response["answer"])


#retrival=rag_pdf(pdf)
#query='Give me the summary of the document'
#answer_generator(retrival,query)