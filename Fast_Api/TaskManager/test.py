from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Integer, Column, String, Index, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

database_url = "sqlite:///./todos.db"

engine = create_engine(database_url,connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index= False)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(engine)

class CreateTodo(BaseModel):
    title: str
    description: str
    completed: bool

class CreateResponse(CreateTodo):
    id: int


@app.post("/todos", response_model=CreateResponse)
def create_todo(todo: CreateTodo):
    db = SessionLocal()
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todo/view", response_model= List[CreateResponse])
def view_todo():
    db = SessionLocal()
    return db.query(Todo).all()

    