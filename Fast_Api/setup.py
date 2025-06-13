from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.get("/addition")
def add(num1: float, num2: float):
    return {"result": num1 + num2}

@app.get("/subtraction")
def subtract(num1: float, num2: float):
    return {"result": num1 - num2}
 
@app.get("/multiplication")
def multiply(num1: float, num2: float):
    return {"result": num1 * num2}

@app.get("/division")
def divide(num1: float, num2: float):
    return {"result": num1 / num2}

