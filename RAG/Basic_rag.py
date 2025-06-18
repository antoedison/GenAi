import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_fixed

# Load environment variables
load_dotenv()
google_api_key = os.getenv("api_key")
os.environ["GOOGLE_API_KEY"] = google_api_key  # important for the underlying SDK

print("🔑 Loaded API key:", (google_api_key[:10] + "...") if google_api_key else "None")

# Step 1: Load Document or URL
def load_data(source: str):
    if source.startswith("http"):
        return WebBaseLoader(source).load()
    elif source.lower().endswith(".pdf"):
        return PyMuPDFLoader(source).load()
    else:
        return TextLoader(source, encoding="utf-8").load()
    


# Step 2: Chunk the Document
def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    return splitter.split_documents(documents)

# Retry logic to handle timeout errors in embedding
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def embed_with_retry(chroma, texts, metadatas):
    chroma.add_texts(texts=texts, metadatas=metadatas)

# Step 3: Create Vector Store
def create_vector_store(chunks, embeddings, batch_size=10):
    all_texts = [doc.page_content.strip() for doc in chunks if doc.page_content.strip()]
    all_metadatas = [doc.metadata for doc in chunks if doc.page_content.strip()]

    # Filter texts that are too short or too long
    filtered_texts = []
    filtered_metadatas = []
    for t, m in zip(all_texts, all_metadatas):
        if 10 < len(t) < 2000:
            filtered_texts.append(t)
            filtered_metadatas.append(m)

    chroma = Chroma(persist_directory="chroma_store", embedding_function=embeddings)

    for i in range(0, len(filtered_texts), batch_size):
        batch_texts = filtered_texts[i:i + batch_size]
        batch_metadatas = filtered_metadatas[i:i + batch_size]

        print(f"🔄 Embedding batch {i // batch_size} with {len(batch_texts)} texts...")
        for j, t in enumerate(batch_texts):
            print(f"  ➤ Chunk {j+1} preview: {t[:100]}...")

        try:
            embed_with_retry(chroma, batch_texts, batch_metadatas)
        except Exception as e:
            print(f"❌ Embedding batch {i // batch_size} failed: {e}")
            continue

    return chroma

# Step 4: Create RAG Pipeline
def build_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a powerful RAG-based assistant. Use the following context to answer the user's question.

Context: {context}

Question: {question}

Answer:
        """
    )

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )
    return rag_chain

# Main pipeline
def main(source_path_or_url, query):
    print("🔍 Loading data...")
    docs = load_data(source_path_or_url)

    print("✂️ Splitting into chunks...")
    chunks = chunk_data(docs)

    print("🔐 Setting up embeddings...")
    # Updated embedding model name — change if your API docs specify another
    embeddings = GoogleGenerativeAIEmbeddings(
        model="embedding-gecko@001",  
        google_api_key=google_api_key
    )

    print("🧠 Creating vectorstore...")
    vectorstore = create_vector_store(chunks, embeddings)

    print("🧬 Building RAG chain...")
    rag_chain = build_rag_chain(vectorstore)

    print("💬 Running RAG Query...")
    result = rag_chain.invoke({"query": query})
    print("\n✅ Answer:\n", result["result"])

# Example usage
if __name__ == "__main__":
    url = "jcc2025131_41733021.pdf"  # Change to your PDF/TXT/URL
    query = "Summarize the entire document"
    main(url, query)
