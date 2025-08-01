import os
import hashlib
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
st.set_page_config(page_title="PDF Assistant", layout="centered",page_icon="https://raw.githubusercontent.com/antoedison/GenAi/main/Showcase/Images/Project_logo.png")

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
def build_vectorstore(chunks, save_path, existing_vectostore=None, batch_size=10):
    all_texts = [doc.page_content.strip() for doc in chunks if doc.page_content.strip()]
    all_metadatas = [doc.metadata for doc in chunks if doc.page_content.strip()]

    filtered_texts = []
    filtered_metadatas = []

    for t, m in zip(all_texts, all_metadatas):
        if 10 < len(t) < 2000:
            filtered_texts.append(t)
            filtered_metadatas.append(m)

    if not filtered_texts:
        raise ValueError("No valid text chunks found for embedding.")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    embedded_documents = []

    for i in range(0, len(filtered_texts), batch_size):
        batch_texts = filtered_texts[i:i + batch_size]
        batch_metadatas = filtered_metadatas[i:i + batch_size]

        print(f"🔄 Embedding batch {i // batch_size + 1} with {len(batch_texts)} texts...")
        for j, t in enumerate(batch_texts):
            print(f"   ➤ Chunk {j + 1} preview: {t[:100]}...")

        embedded_documents.extend([
            Document(page_content=text, metadata=meta)
            for text, meta in zip(batch_texts, batch_metadatas)
        ])

    # ✅ Embedding will be done internally here
    vectorstore = FAISS.from_documents(embedded_documents, embeddings)
    if existing_vectostore:
        existing_vectostore.merge_from(vectorstore)
        existing_vectostore.save_local(save_path)
        return existing_vectostore
    else:
        vectorstore.save_local(save_path)
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

    save_path = "Index_faiss"
    try:
        existing_vectorstore = FAISS.load_local(
            save_path,
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        existing_vectorstore = None

    if uploaded_files:
        all_chunks = []

        for file in uploaded_files:
            text = load_pdf(file)
            with st.spinner("Reading PDFs"):
                pdf_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
                st.write(pdf_hash)
            
            with st.spinner("Splitting text into chunks"):
                chunks = split_text(text)
                
                for chunk in chunks:
                    chunk.metadata["file_name"] = file.name
                    chunk.metadata["pdf_hash"] = pdf_hash
                all_chunks.extend(chunks)
        with st.spinner("🔍 Creating vectorstore..."):
            vectorstore = build_vectorstore(all_chunks,save_path, existing_vectorstore)

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
