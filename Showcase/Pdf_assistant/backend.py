from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
from Pdf_assistant import load_pdf, split_text, build_vectorstore

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

faiss_index_path = "Index_faiss"

embedding = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

if os.path.exists(faiss_index_path):
    db = FAISS.load_local(faiss_index_path,embedding, allow_dangerous_deserialization= True)
    
else:
    db = FAISS.load_local([],embedding, allow_dangerous_deserialization= True)
    


app = FastAPI()



#Get Method
@app.get("/")
def get_chunks():
    try:    
        all_docs : List[Document] = db.similarity_search("",k=1000)
        return {"chunks": [doc.page_content for doc in all_docs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Post Method

@app.post("/Upload_files")
async def upload_pdf(file: UploadFile = File(...)):

    contents = await file.read()
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)
    
    
    text = load_pdf(temp_path)
    chunks = split_text(text)
    new_db = build_vectorstore(chunks, faiss_index_path, db)
    """
    if os.path.exists(faiss_index_path):
        db.merge_from(new_db)
    else:
        db = new_db
    """
    
    db.save_local(faiss_index_path)
    os.remove(temp_path)

    return {"message": "File processed and chunks embedded", "chunks_added": len(chunks)}






