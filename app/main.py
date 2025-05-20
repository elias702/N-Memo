from fastapi import FastAPI

from api import memos
from app.database import engine, Base


app = FastAPI(title="N_Memo", version="1.0.1")

Base.metadata.create_all(engine)

app.include_router(memos.router)
