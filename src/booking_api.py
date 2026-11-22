from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import booking as bk
import booking_agent as ba

router = APIRouter()

class StartBody(BaseModel):
    email: str

class ChatBody(BaseModel):
    session_id: str
    message: str

class ConfirmBody(BaseModel):
    session_id: str
    decision: str

@router.get("/book")
def page():
    return FileResponse("web/book.html")

@router.get("/api/customers")
def customers():
    return [{"email": e, "name": c["name"], "care_plan": c["care_plan"]}
            for e, c in bk.CUSTOMERS.items()]

@router.get("/api/book/bookings")
def bookings(email: str):
    if email not in bk.CUSTOMERS:
        raise HTTPException(404, "Unknown customer")
    return bk.list_bookings(email)          # prod: the email comes from the login session

@router.post("/api/book/start")
def start(b: StartBody):
    if b.email not in bk.CUSTOMERS:
        raise HTTPException(404, "Unknown customer")
    return {"session_id": ba.new_session(b.email)}

@router.post("/api/book/chat")
def chat(b: ChatBody):
    if b.session_id not in ba.SESSIONS:
        raise HTTPException(404, "Unknown session")
    return ba.chat(b.session_id, b.message[:1000])

@router.post("/api/book/confirm")
def confirm(b: ConfirmBody):
    if b.session_id not in ba.SESSIONS:
        raise HTTPException(404, "Unknown session")
    result = ba.confirm(b.session_id, b.decision)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result