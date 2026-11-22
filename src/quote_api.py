from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import quote_agent as qa
from pricing import ACCOUNTS

router = APIRouter()
PARTNER_ROLES = ("partner", "manager", "director")   # prod: roles come from SSO claims

class QuoteBody(BaseModel):
    account_id: str
    message: str
    role: str = "visitor"

class ApproveBody(BaseModel):
    role: str

@router.get("/quote")
def page():
    return FileResponse("web/quote.html")

@router.get("/api/accounts")
def accounts():
    return [{"id": k, "name": v["name"], "tier": v["tier"]} for k, v in ACCOUNTS.items()]

@router.post("/api/quote")
def create(body: QuoteBody):
    if body.role not in PARTNER_ROLES:
        raise HTTPException(403, "Quotes are available to certified partners only")
    if body.account_id not in ACCOUNTS:
        raise HTTPException(404, "Unknown account")
    return qa.create_quote(body.account_id, body.message, body.role)

@router.post("/api/quote/{quote_id}/approve")
def approve(quote_id: str, body: ApproveBody):
    result = qa.approve(quote_id, body.role)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result