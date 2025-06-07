import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from tenacity import retry, stop_after_attempt, wait_fixed

# Load environment variables
load_dotenv()
google_api_key = os.getenv("api_key")

# Step 1: Load Document or URL
def load_data(source: str):
    if source.startswith("http"):
        return WebBaseLoader(source).load()
    else:
        return TextLoader(source, encoding="utf-8").load()

# Step 2: Chunk the Document
def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    return splitter.split_documents(documents)

# Retry logic to handle timeout errors in embedding
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def embed_with_retry(chroma, texts, metadatas):
    chroma.add_texts(texts=texts, metadatas=metadatas)

# Step 3: Create Vector Store
def create_vector_store(chunks, embeddings, batch_size=10):
    all_texts = [doc.page_content for doc in chunks]
    all_metadatas = [doc.metadata for doc in chunks]
    chroma = Chroma(persist_directory="chroma_store", embedding_function=embeddings)

    for i in range(0, len(all_texts), batch_size):
        batch_texts = all_texts[i:i + batch_size]
        batch_metadatas = all_metadatas[i:i + batch_size]
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
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

    print("🧠 Creating vectorstore...")
    vectorstore = create_vector_store(chunks, embeddings)

    print("🧬 Building RAG chain...")
    rag_chain = build_rag_chain(vectorstore)

    print("💬 Running RAG Query...")
    result = rag_chain.invoke({"query": query})
    print("\n✅ Answer:\n", result["result"])

# Example usage
if __name__ == "__main__":
    url = "Current Technological Trends and Fu.txt"
    query = "What are the main goals of artificial intelligence?"
    main(url, query)
