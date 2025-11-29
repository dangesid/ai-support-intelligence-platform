---

# 🤖 AI Support Intelligence Platform

Smart Ticket Classification & Kanban Dashboard for Support Teams

---

## 📌 Overview

The **AI Support Intelligence Platform** is an automated helpdesk solution that uses **Machine Learning** to classify support tickets based on the customer’s issue description.

Users submit tickets from a **customer portal**, and support agents manage them using a **Jira-style Kanban board**, improving team productivity and reducing manual triage.

---

## 🚀 Key Features

✔ AI-powered ticket classification (Bug / Feature / Technical / Account / Payment / etc.).
✔ Customer submission page — clean & easy to use.
✔ Admin dashboard — Kanban drag-and-drop workflow.
✔ Real-time appearance of newly submitted tickets.
✔ Auto-saves ticket status changes to database.
✔ Built using scalable and modular architecture.

---

## 🧠 Tech Stack

| Layer            | Technology                                              |
| ---------------- | ------------------------------------------------------- |
| Backend API      | FastAPI + Uvicorn                                       |
| Machine Learning | Scikit-Learn (Naive Bayes Classifier + CountVectorizer) |
| Database         | SQLAlchemy ORM + SQLite                                 |
| Frontend         | HTML + CSS + JavaScript                                 |
| Model Serving    | Joblib-based inference                                  |

---

## 📂 Project Structure

```
ai-support-intelligence-platform/
├── app/
│   ├── main.py              # FastAPI server + routes
│   ├── models/ticket.py     # DB table model
│   └── database/db.py       # DB engine + session
├── ml/
│   ├── train_ticket_model.py    # Training script
│   ├── inference/model.py       # Load + predict
│   ├── ticket_classifier.pkl    # Trained ML model
├── frontend/
│   ├── index.html           # Customer ticket UI
│   └── admin.html           # Admin Kanban dashboard
├── dataset.csv              # Training dataset
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

```sh
git clone <your-repo-url>
cd ai-support-intelligence-platform
```

### 2️⃣ Create and activate virtual environment

```sh
python3 -m venv venv
source venv/bin/activate   # (Mac/Linux)
# .\venv\Scripts\activate  # (Windows)
```

### 3️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

> If missing, install manually:

```sh
pip install fastapi uvicorn[standard] sqlalchemy scikit-learn pandas joblib python-multipart
```

---

## 🤖 Train Machine Learning Model

Ensure dataset exists:

```
dataset.csv
```

Train classifier:

```sh
python ml/train_ticket_model.py
```

Model saved as:

```
ml/ticket_classifier.pkl
```

---

## ▶️ Run the Server

```sh
uvicorn app.main:app --reload
```

Access UI:

| Page            | URL                                                        |
| --------------- | ---------------------------------------------------------- |
| Customer Portal | [http://127.0.0.1:8000/](http://127.0.0.1:8000/)           |
| Admin Dashboard | [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) |
| API Docs        | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)   |

---

## 🎯 How it Works

1️⃣ Customer submits a ticket from frontend
2️⃣ Text is sent to backend
3️⃣ ML model predicts category
4️⃣ Ticket stored in DB with **predicted category**
5️⃣ Admin dashboard updates automatically when new tickets arrive
6️⃣ Drag-and-drop updates ticket status in DB

---

## 🔮 Future Enhancements (GenAI Roadmap)

| Feature                     | Benefit                              |
| --------------------------- | ------------------------------------ |
| LLM-based ticket auto-reply | Reduce manual response load          |
| RAG with knowledge base     | Auto-suggest solutions               |
| Priority scoring model      | Highlight urgent requests            |
| Multi-agent support         | Automated routing between teams      |
| User roles & authentication | Customer vs Admin dashboards         |
| MLOps Deployment            | CI/CD with AWS / Docker / Monitoring |

---

## 👏 Contributions

PRs and feature suggestions are welcome!
This app will keep growing into a fully-intelligent support system.

---

### ⭐ If you like this project — don't forget to star the repository!

---
