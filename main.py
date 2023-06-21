import fastapi
from sqlalchemy.orm import sessionmaker

from database import engine, Documents

app = fastapi.FastAPI()

s = sessionmaker(bind=engine)
session = s()


@app.get("/first20")
def return_first():
    return [session.get(Documents, i) for i in range(1, 21)]


@app.get("/search/{text}")
def search_text(text: str):
    result = session.query(Documents).filter(Documents.text.like(f"%{text}%")).order_by(Documents.created_date.desc())
    return [doc for doc in result]
