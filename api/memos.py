from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from models import m_model
from schemas import m_schema
from app.database import get_db


router = APIRouter(prefix="/memos", tags=["memos"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/", response_model=m_schema.SMemoCreateResponse, status_code=status.HTTP_200_OK
)
async def create_memo(memo: m_schema.SMemoCreate, db: db_dependency):
    memo_model = m_model.Memo(**memo.model_dump())
    db.add(memo_model)
    db.commit()
    db.refresh(memo_model)
    return memo_model


@router.get(
    "/{memo_id}", response_model=m_schema.SMemoResponse, status_code=status.HTTP_200_OK
)
async def read_memo(db: db_dependency, memo_id: int = Path(gt=0)):
    memo_model = db.query(m_model.Memo).filter(m_model.Memo.id == memo_id).first()
    if memo_model is None:
        raise HTTPException(status_code=404, detail="Memo not found!")
    return memo_model


@router.get(
    "/", response_model=list[m_schema.SMemoResponse], status_code=status.HTTP_200_OK
)
async def read_all_memo(db: db_dependency, skip: int = 0, limit: int = 25):
    memo_model = db.query(m_model.Memo).offset(skip).limit(limit).all()
    return memo_model
