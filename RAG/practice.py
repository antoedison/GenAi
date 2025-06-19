import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import streamlit as st
from langchain_community.vectorstores import FAISS 
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQa 

os.environ["GOOGLE_API_KEY"] = "AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90"

# Set page config
st.set_page_config(page_title="PDF Assistant", layout="centered")

with st.sidebar:
    st.title("PDF Assistant")
    st.markdown("""
    Upload a PDF and ask questions about it
                """)
    
    
def pdf_loader(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text+= page.extract_text()
    return text

def split_text(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 300,
        chunk_overlap = 50
    )
    return splitter.create_documents([text])

def build_vectorstore(documents):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_documents(documents, embeddings)

def create_qa_chain(vectorstores):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        convert_system_message_to_human=True
    )
    return RetrievalQa.from_chain_type(
        llm = llm,
        retriver = vectorstores.as_retriever(),
        return_source_documents = True
    )

def main():
    st.header(" PDF Question answering app")
    uploade_file = st.file_uploader("Upload a PDF", type = "pdf")

    if uploade_file:
        with st.spinner("Reading PDF..."):
            


