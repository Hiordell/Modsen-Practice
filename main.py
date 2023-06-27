import fastapi
from sqlalchemy.orm import sessionmaker
import elastic_transport
from elasticsearch import Elasticsearch

from database import engine, Documents
from config import ES_HOST, ES_PORT

app = fastapi.FastAPI()

s = sessionmaker(bind=engine)
session = s()

es = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")


@app.delete("/delete-all-docs")
async def delete_all_data():
    try:
        session.query(Documents).delete()
        session.flush()
        session.commit()

        es.delete_by_query(index="documents", body={"query": {"match_all": {}}})
    except elastic_transport.ConnectionTimeout:
        session.rollback()



@app.get("/elastic-search/{doc_text}")
async def elastic_search(doc_text: str):
    resp = es.search(
        index="documents",
        size=20,
        query={
            "match": {
                    "text": doc_text,
                },
        },
    )

    doc_ids = [int(hit["_source"]["id"]) for hit in resp['hits']['hits']]
    return [doc for doc in session.query(Documents).filter(Documents.id.in_(doc_ids)).order_by(Documents.created_date.desc())]


@app.delete("/delete-doc/{doc_id}")
async def delete_doc(doc_id: int):
    try:
        session.query(Documents).filter(Documents.id == doc_id).delete()
        session.commit()

        es.delete_by_query(index="documents", body={
            "query": {
                "match": {
                    "id": doc_id
                }
            }
        })
    except elastic_transport.ConnectionTimeout:
        session.rollback()


@app.post("/add-doc")
async def add_doc(body=fastapi.Body()):
    try:
        doc = Documents(body)
        session.add(doc)
        session.flush()
        session.refresh(doc)
        session.commit()

        doc = {
            "id": doc.id,
            "text": doc.text
        }
        es.index(index="documents", document=doc)
    except elastic_transport.ConnectionTimeout:
        session.rollback()
