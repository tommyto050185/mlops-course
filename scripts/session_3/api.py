from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel # type: ignore

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

class CalculateRequest(BaseModel):
    method: str
    num1: float
    num2: float
class CalculateResponse(BaseModel):
    result: float


@app.post(f"/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest)-> CalculateResponse:    
    if  request.method == "add":
        result = request.num1 + request.num2
    elif request.method == "subtract":
        result = request.num1 - request.num2
    elif request.method == "multiply":
        result = request.num1 * request.num2
    elif request.method == "divide":
        result = request.num1 / request.num2
    return CalculateResponse(result=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 