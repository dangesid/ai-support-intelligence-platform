import joblib

# Load trained model
model = joblib.load("ml/ticket_classifier.pkl")

def predict_category(text: str):
    return model.predict([text])[0]