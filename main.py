from fastapi import FastAPI, Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from api import memos
from dev.database import engine, Base, get_db
from models import m_model
from schemas import m_schema


app = FastAPI(title="N_Memo", version="1.0.1")

app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")


Base.metadata.create_all(engine)

app.include_router(memos.router)


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    context = {"request": request, "title": "Native Memo"}
    return template.TemplateResponse("landing.html", context)


@app.get("/dashboard/", response_class=HTMLResponse)
async def read_dashboard_page(request: Request, db: Session = Depends(get_db)):

    memos_data = (
        db.query(m_model.Memo).order_by(m_model.Memo.created_at.desc()).limit(25).all()
    )
    validated_memos = [
        m_schema.SMemoUpdateResponse.model_validate(memo) for memo in memos_data
    ]
    context = {
        "request": request,
        "title": "User Dash- N-MEMO",
        "user_name": "Guest",
        "memos": validated_memos,
    }
    return template.TemplateResponse("dashboard.html", context)


@app.get("/my_memo/", response_class=HTMLResponse)
async def my_memo_page(request: Request, db: Session = Depends(get_db)):
    memos_data = (
        db.query(m_model.Memo).order_by(m_model.Memo.created_at.desc()).limit(25).all()
    )
    validated_memos = [
        m_schema.SMemoUpdateResponse.model_validate(memo) for memo in memos_data
    ]

    context = {
        "request": request,
        "title": "My Memo - N-Memo",
        "memos": validated_memos,
    }
    return template.TemplateResponse("mymemo.html", context)
