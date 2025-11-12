

from fastapi import FastAPI 
import uvicorn
from pydantic import BaseModel
from enum import Enum
import os
import joblib


#import model/housing_linear_regression_model_01

#import scripts.session_3.router.house_price_prediction as house_price_prediction_router

app = FastAPI()
#app.include_router(house_price_prediction_router.hpp_router)

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




class PredictRequest(BaseModel):
    avg_Area_Income: float
    avg_Area_House_Age: float
    avg_Area_Number_of_Rooms: float
    avg_Area_Number_of_Bedrooms: float
    avg_Area_Population: float

class PredictResponse(BaseModel):
    predicted_Price: float
# build model truc tiep
model = joblib.load("./housing_linear.joblib")
@app.post(f"/predict", response_model=PredictResponse)
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


if __name__ == "__main__":
    
   
    #port = int(os.environ.get("PORT", 3000))
    #uvicorn.run("main:app", host="0.0.0.0", port=port)
    uvicorn.run(app, host="0.0.0.0", port=3000)