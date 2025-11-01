from fastapi import FastAPI 
import uvicorn
from pydantic import BaseModel
from enum import Enum
#import model/housing_linear_regression_model_01

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

# sample_data = {
#         "Avg. Area Income": [120000],
#         "Avg. Area House Age": [12],
#         "Avg. Area Number of Rooms": [8],
#         "Avg. Area Number of Bedrooms": [4],
#         "Area Population": [75000],
#     }
class PredictRequest(BaseModel):
    avg_Area_Income: float
    avg_Area_House_Age: float
    avg_Area_Number_of_Rooms: float
    avg_Area_Number_of_Bedrooms: float
    avg_Area_Population: float

class PredictResponse(BaseModel):
    predicted_Price: float

### CACH 1: SU DUNG MODEL TU MFLOW 
import mlflow.sklearn
mlflow.set_tracking_uri("http://localhost:8080")
model_name = "housing_linear_regression_model_01"
model_version = "2"
model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.sklearn.load_model(model_uri)
@app.post(f"/predict_house_price", response_model=PredictResponse)
def predict_house_price(request: PredictRequest)-> PredictResponse:   
    import pandas as pd
    sample_data = {
        "Avg. Area Income": [request.avg_Area_Income],
        "Avg. Area House Age": [request.avg_Area_House_Age],
        "Avg. Area Number of Rooms": [request.avg_Area_Number_of_Rooms],
        "Avg. Area Number of Bedrooms": [request.avg_Area_Number_of_Bedrooms],
        "Area Population": [request.avg_Area_Population],
    }
    df = pd.DataFrame(sample_data)
    predictions = model.predict(df)
    return PredictResponse(predicted_Price=predictions[0])
    ### CACH 2: SU DUNG MODEL DA BUILT-IN MLRUNS


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 