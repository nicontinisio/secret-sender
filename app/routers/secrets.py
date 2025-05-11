from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import uuid, json, base64
from ..config import settings
from ..db import db
from ..crypto import encrypt
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/secrets", response_class=HTMLResponse)
async def create_secret(request: Request,
                        message: str = Form(...),
                        ttl_choice: str = Form(""),
                        password: str = Form(None),
                        file: UploadFile = File(None)):
    ttl_map = {'': None, '1h':3600, '24h':86400, '1d':86400, '30d':2592000}
    ttl = ttl_map.get(ttl_choice)
    token = uuid.uuid4().hex
    payload = {"message": message}
    if file:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_BYTES:
            raise HTTPException(413, f"File troppo grande (max {settings.MAX_UPLOAD_MB} MB)")
        payload.update({"filename": file.filename, "filedata": base64.b64encode(content).decode()})
    blob = encrypt(json.dumps(payload).encode(), password)
    raw = json.dumps(blob).encode()
    if ttl:
        db.setex(token, ttl, raw)
    else:
        db.set(token, raw)
    return templates.TemplateResponse("fragment.html", {"request": request, "token": token})