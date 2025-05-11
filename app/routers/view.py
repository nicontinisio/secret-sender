from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
import json
from ..db import db
from ..crypto import decrypt
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/secrets/{token}", response_class=HTMLResponse)
def view_secret(request: Request, token: str):
    raw = db.get(token)
    if not raw:
        return templates.TemplateResponse("view.html", {"request": request, "error": "Secret non trovato o già letto"})
    blob = json.loads(raw)
    return templates.TemplateResponse("view.html", {"request": request,
                                                    "token": token,
                                                    "needs_pw": blob['enc_pw'],
                                                    "blob": json.dumps(blob)})

@router.post("/secrets/{token}", response_class=HTMLResponse)
async def unlock_secret(request: Request, token: str, password: str = Form(None)):
    form = await request.form()
    blob = json.loads(form['blob'])
    try:
        plaintext = decrypt(blob, password)
    except HTTPException as e:
        return templates.TemplateResponse("view.html", {"request": request,
                                                         "token": token,
                                                         "needs_pw": blob['enc_pw'],
                                                         "blob": json.dumps(blob),
                                                         "error": e.detail})
    db.delete(token)
    data = json.loads(plaintext)
    file_info = {"name": data['filename'], "data": data['filedata']} if 'filedata' in data else None
    return templates.TemplateResponse("view.html", {"request": request,
                                                      "message": data['message'],
                                                      "file": file_info,
                                                      "revealed": True,
                                                      "token": token})