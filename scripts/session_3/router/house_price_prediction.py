from pydantic import BaseModel
from fastapi import APIRouter


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

hpp_router = APIRouter(prefix="/ml-predict")
@hpp_router.post(f"/house_price", response_model=PredictResponse)
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
