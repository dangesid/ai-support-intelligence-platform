import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

print("Loading data...")

data = pd.read_csv("dataset.csv")

# combine title and description
data["text"] = data["title"] + " " + data["description"]

X = data["text"]
y = data["category"]

print("Dataset Loaded ")
print("Total Samples: ", len(data))

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create ML Pipeline 
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=1000))
])

print("Training model...")
model.fit(X_train, y_train)

#Evaluate Model
y_pred = model.predict(X_test)
Accuracy = accuracy_score(y_test, y_pred)

print("\n Model Accuracy:", Accuracy)
print("\n Classification Report:\n", classification_report(y_test, y_pred))

#saving model 
joblib.dump(model, "ml/ticket_classifier.pkl")

print("Model saved as ml/ticket_classifier.pkl")