from fastapi import FastAPI # type: ignore
import uvicorn # type: ignore
from pydantic import BaseModel # type: ignore
from enum import Enum

app = FastAPI()

@app.get(f"/")
def root():
    return {"message": "Hello World from FastAPI!"}

@app.get(f"/health")
def health(num_input: int):
    if num_input > 10:
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}

class Method(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class CalculateRequest(BaseModel):
    method: Method
    num1: float
    num2: float
class CalculateResponse(BaseModel):
    result: float


@app.post(f"/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest)-> CalculateResponse:    
    if  request.method == Method.add:
        result = request.num1 + request.num2
    elif request.method == Method.subtract:
        result = request.num1 - request.num2
    elif request.method == Method.multiply:
        result = request.num1 * request.num2
    elif request.method == Method.divide:
        result = request.num1 / request.num2
    return CalculateResponse(result=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 