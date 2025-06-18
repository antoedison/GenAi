import os
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# 🔐 Set API key directly in the code
os.environ["GOOGLE_API_KEY"] = "AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90"

# 1. Load PDF and extract text
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 2. Split text into smaller chunks
def split_text(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=50
    )
    return splitter.create_documents([text])

# 3. Embed and store in vector DB
def build_vectorstore(documents):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# 4. Create a RetrievalQA chain
def create_qa_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2,convert_system_message_to_human=True)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    return qa_chain

# 5. Main RAG flow
def main():
    pdf_path = "jcc2025131_41733021.pdf"  # Replace with your actual file
    print("📄 Loading PDF...")
    text = load_pdf(pdf_path)

    print("✂️ Splitting text...")
    docs = split_text(text)

    print("🔍 Creating vectorstore...")
    vectorstore = build_vectorstore(docs)

    print("🧠 Creating QA chain...")
    qa = create_qa_chain(vectorstore)

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        result = qa.invoke(query)
        print("\nAnswer:\n", result["result"])

if __name__ == "__main__":
    main()
