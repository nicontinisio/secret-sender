from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .config import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
templates.env.globals.update({
    'MAX_UPLOAD_MB': settings.MAX_UPLOAD_MB,
    'MAX_UPLOAD_BYTES': settings.MAX_UPLOAD_BYTES
})

# Root endpoint
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include routers
from .routers import secrets, view, about
app.include_router(secrets.router)
app.include_router(view.router)
app.include_router(about.router)