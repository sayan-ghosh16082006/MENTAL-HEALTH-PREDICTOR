import requests
import joblib
from io import BytesIO
import pandas as pd





MODEL_PATH = "https://huggingface.co/sayan2006/Mental_Health_Predictor_Model/resolve/main/model.pkl"

def load_model():
    response = requests.get(MODEL_PATH)
    return joblib.load(BytesIO(response.content))


model = load_model()




def predict_output(user_input:dict):

    input_df = pd.DataFrame([user_input])
    output = model.predict(input_df)[0]

    return  {"Predicted Score" : round(output, 2)}