"""
FastAPI backend for Todo Task Manager
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLAlchemy ORM Model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# Pydantic model
class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int

# Routes
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    db = SessionLocal()
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos():
    db = SessionLocal()
    return db.query(Todo).all()

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
