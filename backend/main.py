from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.api_schema import InputData, PredictedResponse
from backend.prediction import predict_output






app = FastAPI(title="Mental Health Predictor")



@app.get("/")
def home():
    return {"message" : "Mental Health Prediction"}


@app.get("/health")
def health_check():
    return {"Status" : "Ok"}


@app.post("/predict", response_model=PredictedResponse)
def predict(data : InputData):
    user_input = {
        'Age'                               : data.Age,
        'Gender'                            : data.Gender,
        'Country'                           : data.Country,
        'Academic_Level'                    : data.Academic_Level,
        'Most_Used_Platform'                : data.Most_Used_Platform,
        'Purpose_Of_Use'                    : data.Purpose_Of_Use,
        'Avg_Daily_Usage_Hours'             : data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks'                     : data.Daily_Unlocks,
        'Study_Hours'                       : data.Study_Hours,
        'Physical_Activity_Hours'           : data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night'             : data.Sleep_Hours_Per_Night,
        'Stress_Level'                      : data.Stress_Level
    }
    

    try:
        prediction = predict_output(user_input)

        return JSONResponse(status_code = 200, content = {"response" : prediction})
    except Exception as e:
        return JSONResponse(status_code = 500, content = {"error" : str(e)})
