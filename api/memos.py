from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated, List
from starlette import status

from models import m_model
from schemas import m_schema
from dev.database import get_db


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
    "/{memo_id}",
    response_model=m_schema.SMemoUpdateResponse,
    status_code=status.HTTP_200_OK,
)
async def read_memo(db: db_dependency, memo_id: int = Path(gt=0)):
    memo_model = db.query(m_model.Memo).filter(m_model.Memo.id == memo_id).first()
    if memo_model is None:
        raise HTTPException(status_code=404, detail="Memo not found!")

    if memo_model.updated_at:
        return m_schema.SMemoUpdateResponse.model_validate(memo_model)
    return m_schema.SMemoCreateResponse.model_validate(memo_model)
    # return memo_model


@router.get(
    "/",
    # response_model=List[m_schema.SMemoUpdateResponse],
    status_code=status.HTTP_200_OK,
)
async def read_all_memo(db: db_dependency, skip: int = 0, limit: int = 25):
    memo_model = db.query(m_model.Memo).offset(skip).limit(limit).all()

    result = []
    for memo in memo_model:
        if memo.updated_at:
            result.append(m_schema.SMemoUpdateResponse.model_validate(memo))
        else:
            result.append(m_schema.SMemoCreateResponse.model_validate(memo))
    return result


@router.patch(
    "/{memo_id}",
    # response_model=m_schema.SMemoUpdateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_memo(
    db: db_dependency, memo: m_schema.SMemoPartialUpdate, memo_id: int = Path(gt=0)
):
    memo_model = db.query(m_model.Memo).filter(m_model.Memo.id == memo_id).first()

    if memo_model is None:
        raise HTTPException(status_code=404, detail="Memo not found!")

    # check if any update occurred to set updated_at
    updated_fields = False

    if memo.title is not None:
        memo_model.title = memo.title
        updated_fields = True
    if memo.content is not None:
        memo_model.content = memo.content
        updated_fields = True

    if updated_fields:  # if actual changes were made
        memo_model.updated_at = datetime.now()

    db.add(memo_model)
    db.commit()
    db.refresh(memo_model)

    return memo_model


@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memo(db: db_dependency, memo_id: int = Path(gt=0)):
    memo_model = db.query(m_model.Memo).filter(m_model.Memo.id == memo_id).first()

    if memo_model is None:
        raise HTTPException(status_code=404, detail="Memo not found!")

    db.delete(memo_model)
    db.commit()
