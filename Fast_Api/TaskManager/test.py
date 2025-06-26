from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

db_file = 'db.json'

class Task(BaseModel):
    task_name: str
    task_description: str
    Completed: bool

def load_db():
    try:
        with open(db_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return[]
    
def save_db():
    try:
        with open(db_file,'w') as file:
            json.dump(db, file)
    except FileNotFoundError:
        return []

@app.get("/task")
def Get_data():
    return load_db()


@app.post("/task/create")
def create_task(task_id: int, task: Task):
    db = load_db()
    db.append(task.Task)
    save_db()
    return {"message": "Task created"}

