from fastapi import FastAPI, Query, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from starlette import status

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
        "title": "N-MEMO -userDash",
        "user_name": "Guest",
        "memos": validated_memos,
    }
    return template.TemplateResponse("dashboard.html", context)


@app.get("/create_memo/", response_class=HTMLResponse)
async def create_memo_form(request: Request, msg: str = None, error: str = None):
    context = {
        "request": request,
        "title": "N-Memo -createMemo",
        "msg": msg,
        "error": error,
    }
    return template.TemplateResponse("creatememo.html", context)


@app.post("/create_memo/", response_class=HTMLResponse)
async def create_submit(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(),
    content: str = Form(),
):
    if not title.strip() or not content.strip():
        return RedirectResponse(
            url=app.url_path_for("create_memo_form")
            + "?error=Title and content cannot be empty.",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    try:
        new_memo = m_model.Memo(title=title, content=content, created_at=datetime.now())
        db.add(new_memo)
        db.commit()
        db.refresh(new_memo)

        return RedirectResponse(
            url=app.url_path_for("my_memo_page") + "?msg=Memo created successfully!",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        db.rollback()
        return RedirectResponse(
            url=app.url_path_for("create_memo_form")
            + f"?error=Failed to create memo: {e}",
            status_code=status.HTTP_303_SEE_OTHER,
        )


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
        "title": "N-Memo -myMemo",
        "memos": validated_memos,
    }
    return template.TemplateResponse("mymemo.html", context)


@app.get("/all_memo/", response_class=HTMLResponse)
async def all_memo_page(request: Request, db: Session = Depends(get_db)):
    memos_data = (
        db.query(m_model.Memo).order_by(m_model.Memo.created_at.desc()).limit(25).all()
    )
    validated_memos = [
        m_schema.SMemoUpdateResponse.model_validate(memo) for memo in memos_data
    ]

    context = {
        "request": request,
        "title": "N-Memo -allMemo",
        "memos": validated_memos,
    }
    return template.TemplateResponse("allmemo.html", context)
