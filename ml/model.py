import joblib
import os

# abs path to model file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ticket_classifier.pkl')

# Load the model once at startup 
model = joblib.load(MODEL_PATH)

def predict_category(text: str):
    return model.predict([text])[0]