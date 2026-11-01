# Mental Health Predictor

A full-stack machine learning application that estimates a student's mental health score based on daily habits, social media usage, sleep, study load, and stress indicators. The project combines a FastAPI backend with a Streamlit dashboard so users can enter lifestyle details and get a quick health-risk-style estimate.

## Overview

This project is designed to predict a mental health score from behavioral inputs rather than provide a medical diagnosis. It uses a pre-trained scikit-learn model and exposes it through a REST API and a user-friendly front-end interface.

The app accepts inputs such as:

- Age
- Gender
- Country
- Academic level
- Most used social media platform
- Primary purpose of use
- Daily usage hours
- Daily phone unlocks
- Study hours
- Physical activity hours
- Sleep hours
- Stress level

The result is a score on a roughly 0–10 scale, interpreted through the UI as:

- Needs attention
- Moderate
- Healthy

## Tech Stack

- Python
- FastAPI
- Streamlit
- scikit-learn
- pandas
- NumPy
- Plotly
- joblib
- requests
- Matplotlib and Seaborn

## Project Structure

```text
Mental_Health_Predictor/
├── backend/
│   ├── api_schema.py        # Pydantic request/response models
│   ├── main.py              # FastAPI app and routes
│   └── prediction.py        # model loading and prediction logic
├── frontend/
│   └── app.py               # Streamlit UI for prediction inputs/results
├── data/
│   └── Student Social Media And Mental Health Impact.csv
├── ipynb_notebooks/
│   └── data_preprocessing.ipynb
├── .gitignore
├── model.pkl                # trained model artifact
├── requirements.txt
├── readme.md
└── .venv                    # local virtual environment
```

## Dataset

The project uses a CSV dataset named `Student Social Media And Mental Health Impact.csv` stored in the `data/` folder. It includes variables relevant to student well-being such as age, gender, country, academic level, social media usage, study hours, physical activity, sleep, stress, and the target variable `Mental_Health_Score`.

## Model and Prediction Flow

The backend loads a serialized model from Hugging Face using `joblib`:

- `backend/prediction.py`
- `MODEL_PATH = "https://huggingface.co/sayan2006/Mental_Health_Predictor_Model/resolve/main/model.pkl"`

The flow is:

1. User submits form values in the Streamlit app
2. Frontend sends a POST request to the FastAPI API
3. FastAPI validates input using `backend/api_schema.py`
4. `backend/prediction.py` builds a DataFrame and runs the model
5. Response is returned as a JSON object with the predicted score

## Getting Started

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
cd D:\CODING\Virtual_py\PROJECTS\Mental_Health_Predictor
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the backend API

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API endpoints include:

- `GET /` - basic welcome response
- `GET /health` - health check
- `POST /predict` - prediction endpoint

### 4. Start the frontend

In a second terminal:

```powershell
streamlit run frontend\app.py
```

Then open the local Streamlit URL shown in the terminal, usually `http://localhost:8501`.

## API Example

Example request body for `POST /predict`:

```json
{
  "Age": 21,
  "Gender": "Male",
  "Country": "India",
  "Academic_Level": "Undergraduate",
  "Most_Used_Platform": "Instagram",
  "Purpose_Of_Use": "Entertainment",
  "Avg_Daily_Usage_Hours": 5.5,
  "Daily_Unlocks": 180,
  "Study_Hours": 4.0,
  "Physical_Activity_Hours": 1.5,
  "Sleep_Hours_Per_Night": 6.5,
  "Stress_Level": "Medium"
}
```

Example response:

```json
{
  "response": {
    "Predicted Score": 6.82
  }
}
```

## Frontend Behavior

The Streamlit app features:

- structured input form for lifestyle data
- gauge-style result display
- colour-coded interpretation bands
- message cards with general guidance based on score ranges

## Important Notes

- This application is an educational and prototype-style mental wellness estimator.
- It is not a clinical diagnosis tool and should not replace professional medical advice.
- The score is derived from statistical correlations in the training data and is meant to encourage self-reflection, not medical treatment.

## Future Improvements

Potential next steps for this project include:

- adding a training notebook or reproducible training script
- saving and versioning the model locally
- adding better explainability and feature importance charts
- supporting more demographic and health metrics
- improving validation and model performance monitoring

## License

This project does not currently specify a formal license in the repository. If you plan to reuse or distribute it, add a suitable open-source license before publishing.
