from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from typing import List
import os
from dotenv import load_dotenv
from Rag_utils import load_pdf, split_text, build_vectorstore
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # ✅ fixed typo here
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load environment variable
google_api_key = os.getenv("GOOGLE_API_KEY")

# Set vector store path
faiss_index_path = "Index_faiss"

# Embedding model
embedding = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

# Load existing FAISS index if present
db = None
if os.path.exists(faiss_index_path):
    db = FAISS.load_local(faiss_index_path, embedding, allow_dangerous_deserialization=True)

# GET method to list all chunks
@app.get("/")
def get_chunks():
    try:
        all_docs: List[Document] = db.similarity_search("", k=1000)
        return {"chunks": [doc.page_content for doc in all_docs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST method to upload PDF file as raw bytes (not multipart)
"""
@app.post("/Upload_files")
async def upload_raw_pdf(request: Request):
    try:
        body = await request.body()
        filename = "uploaded.pdf"  # Static temp file name

        with open(filename, "wb") as f:
            f.write(body)

        text = load_pdf(filename)
        chunks = split_text(text)
        new_db = build_vectorstore(chunks, faiss_index_path, db)

        # Save new or updated DB
        new_db.save_local(faiss_index_path)

        # Cleanup
        os.remove(filename)

        return {"message": "File processed and chunks embedded", "chunks_added": len(chunks)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

@app.post("/Upload_files")
async def upload_file(request: Request, x_filename: str = Header(None)):
    file_bytes = await request.body()

    # Save the file (optional)
    with open(x_filename, "wb") as f:
        f.write(file_bytes)

    # Do something with the file bytes (e.g. parse PDF)

    text = load_pdf(x_filename)

    all_chunks = split_text(text)

    vectorstore = build_vectorstore(all_chunks,faiss_index_path,db)


    return JSONResponse(content={
        "message": f"File '{x_filename}' received successfully!",
        "chunks_added": len(all_chunks)  # Example
    })
