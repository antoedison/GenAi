from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Integer, Column, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins — restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- Database Setup ---
database_url = "sqlite:///./todos.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# --- SQLAlchemy Model ---
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=False)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# --- Pydantic Models ---
class CreateTodo(BaseModel):
    title: str
    description: str
    completed: bool

class CreateResponse(CreateTodo):
    id: int

# --- Create Task ---
@app.post("/todo/create", response_model=CreateResponse)
def create_todo(todo: CreateTodo):
    db = SessionLocal()
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.close()
    return db_todo

# --- View Tasks ---
@app.get("/todo/view", response_model=Liscdt[CreateResponse])
def view_todo():
    db = SessionLocal()
    tasks = db.query(Todo).all()
    db.close()
    return tasks

# --- Update Task ---
@app.put("/todo/update/{todo_id}", response_model=CreateResponse)
def update_todo(todo_id: int, updated_todo: CreateTodo):
    db = SessionLocal()
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_item:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_item.title = updated_todo.title
    todo_item.description = updated_todo.description
    todo_item.completed = updated_todo.completed

    db.commit()
    db.refresh(todo_item)
    db.close()
    return todo_item

# --- Delete Task ---
@app.delete("/todo/delete/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_item:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_item)
    db.commit()
    db.close()
    return {"message": f"Todo with id {todo_id} deleted successfully"}