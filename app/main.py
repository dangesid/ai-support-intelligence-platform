from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine, SessionLocal
from app.models.ticket import SupportTicket
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles

from ml.inference.model import predict_category

# FastAPI app instance
app = FastAPI(title="AI Support Intelligence Platform")


# Allow frontend JS calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve frontend index.html at root
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

@app.get("/admin")
def serve_admin():
    return FileResponse(os.path.join("frontend", "admin.html"))

# Optional: serve other static assets (JS/CSS/images) under /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Databse Setup initialization
Base.metadata.create_all(bind=engine)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

# Pydantic models
class TicketCreate(BaseModel):
    title: str
    description: str


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category: str


# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


#Flag for admin UI update events
new_ticket_flag = False

@app.get("/check-updates")
def check_updates():
    """Admin calls this repeatedly — only get TRUE when a new ticket arrives"""
    return {"update": new_ticket_flag}

@app.post("/reset-updates")
def reset_updates():
    """Reset flag after UI refresh"""
    global new_ticket_flag
    new_ticket_flag = False
    return {"message": "reset"}

#--------------------------------------------
### CRUD Endpoints for Support Tickets ###   |
#--------------------------------------------

# Create new ticket
@app.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    full_text = f"{ticket.title} {ticket.description}"

    ai_category = predict_category(full_text)

    new_ticket = SupportTicket(
        title=ticket.title,
        description=ticket.description,
        category=ai_category,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

# List all tickets
@app.get("/tickets", response_model=List[TicketOut])
def list_ticket(db: Session = Depends(get_db)):
    return db.query(SupportTicket).all()

# Update ticket status
@app.patch("/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket_status(ticket_id: int, payload: dict, db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = payload.get("status", ticket.status)
    db.commit()
    db.refresh(ticket)
    return ticket

@app.post("/predict-category")
def predict(ticket: dict):
    text = ticket.get("title", "") + " " + ticket.get("description", "")
    category = predict_category(text)
    return {"predicted_category": category}
