from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Root directory
@app.get("/")
def read_root():
    return {'message':'Hello! World'}

db= {
    1 :{
        'task_name':'Running',
        'task_description':'To keep the body fit',
        'Completed': True        
    }
}

class create_db(BaseModel):
    task_name: str
    task_description: str
    Completed: bool

class update_db(BaseModel):
    task_name: str
    task_description: str
    Completed: bool

#Get by id
@app.get("/task/{task_id}")
def get_data(task_id: int):
    if task_id  not in db:
        return {'Error': 'Task Id does not exist'}
    return db[1]

@app.post("/task/create/{task_id}")
def create_task(task_id: int, task: create_db):
    if task_id in db:
        return {'Error': 'Task Id already exists'}
    db[task_id] = task
    return db[task_id]

@app.put("/task/update/{task_id}")
def update_task(task_id: int, task: update_db):
    if task_id not in db:
        return {'Error': 'Task Id does not exist'}
    if task.task_name != None:
        db[task_id]['task_name'] = task.task_name
    if task.task_description != None:
        db[task_id]['task_description'] = task.task_description
    if task.Completed != None:
        db[task_id]['Completed'] = task.Completed
    return db[task_id]

@app.delete("/task/delete/{task_id}")
def delete_task(task_id: int):
    if task_id not in db:
        return {'Error': 'Task Id does not exist'}
    del db[task_id]

