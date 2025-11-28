import pandas as pd 
from sqlalchemy.orm import Session 
from app.database.db import SessionLocal
from app.models.ticket import SupportTicket
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load Tickets from DB 

db: Session = SessionLocal()
tickets = db.query(SupportTicket).all() 
db.close()

# Convert to DataFrame
data = pd.DataFrame([{
    "id": t.id,
    "title": t.title,
    "description": t.description,
    "category": t.category
} for t in tickets])

# Encode Labels 
le = LabelEncoder()
data['category_label'] = le.fit_transform(data['category'])

# Text Embeddings using SentenceTransformer
model_embed = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model_embed.encode(data['description'].tolist())

# Spliting data
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, data['category_label'], test_size=0.2, random_state=42
)

# Train classifier 
clf = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
clf.fit(X_train, y_train)

# Save the trained model and label encoder
joblib.dump(clf, 'ml/ticket_classifier_model.joblib')
joblib.dump(le, 'ml/label_encoder.joblib')
joblib.dump(model_embed, 'ml/sentence_transformer_model.joblib')

# Save FAISS index for embeddings
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings).astype('float32'))
faiss.write_index(index, 'ml/faiss_ticket_index.index')

print(" Training completed, Model, encoder, embedding saved. ")