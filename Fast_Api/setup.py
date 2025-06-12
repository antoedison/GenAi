from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.get("/addition")
def add(num1: float, num2: float):
    return {"result": num1 + num2}


