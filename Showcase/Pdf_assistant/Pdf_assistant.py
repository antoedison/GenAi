import os
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.schema import Document  # ✅ Missing import fixed

# 🔐 Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90"

# Set page config
st.set_page_config(page_title="PDF Assistant", layout="centered",page_icon="D:\Virtusa_Internship\Showcase\Images\Project_logo.png")

# Sidebar
with st.sidebar:
    st.title("📄 PDF Assistant")
    st.markdown("""
    Upload one or more PDFs and ask questions about them!
    
    Powered by:
    - Google Generative AI
    - LangChain
    - FAISS VectorStore
    """)

# Function to load PDF
def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Split text into chunks
def split_text(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=50
    )
    return splitter.create_documents([text])

# Create FAISS vectorstore with batching and filtering
def build_vectorstore(chunks, batch_size=10):
    all_texts = [doc.page_content.strip() for doc in chunks if doc.page_content.strip()]
    all_metadatas = [doc.metadata for doc in chunks if doc.page_content.strip()]

    filtered_texts = []
    filtered_metadatas = []

    for t, m in zip(all_texts, all_metadatas):
        if 10 < len(t) < 2000:
            filtered_texts.append(t)
            filtered_metadatas.append(m)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    embedded_documents = []

    for i in range(0, len(filtered_texts), batch_size):
        batch_texts = filtered_texts[i:i + batch_size]
        batch_metadatas = filtered_metadatas[i:i + batch_size]

        print(f"🔄 Embedding batch {i // batch_size + 1} with {len(batch_texts)} texts...")
        for j, t in enumerate(batch_texts):
            print(f"   ➤ Chunk {j + 1} preview: {t[:100]}...")

        batch_documents = [Document(page_content=t, metadata=m) for t, m in zip(batch_texts, batch_metadatas)]
        embedded_documents.extend(batch_documents)

    vectorstore = FAISS.from_documents(embedded_documents, embeddings)
    return vectorstore

# Create RetrievalQA chain
def create_qa_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, convert_system_message_to_human=True)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs = {"k": 10}),
        return_source_documents=True
    )

# Main app function
def main():
    st.header("🧠 PDF Question Answering App")
    uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        with st.spinner("📄 Reading PDFs..."):
            full_text = ""
            for file in uploaded_files:
                full_text += load_pdf(file)

        with st.spinner("✂️ Splitting text into chunks..."):
            docs = split_text(full_text)

        with st.spinner("🔍 Creating vectorstore..."):
            vectorstore = build_vectorstore(docs)

        with st.spinner("🧠 Setting up QA chain..."):
            qa = create_qa_chain(vectorstore)

        st.success("✅ PDFs processed! You can now ask your questions below.")

        query = st.text_input("💬 Ask a question about the PDFs")
        if query:
            with st.spinner("🤔 Thinking..."):
                result = qa.invoke(query)

            st.markdown("### ✅ Answer")
            st.write(result["result"])

            with st.expander("📚 Source Documents"):
                for doc in result["source_documents"]:
                    st.markdown(f"**Content Preview:** {doc.page_content[:300]}...")

    else:
        st.info("👈 Please upload at least one PDF to get started.")

# Run the app
if __name__ == "__main__":
    main()
