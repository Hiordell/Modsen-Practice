import operator

import fastapi
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch
import pandas

from database import engine, Documents
from config import ES_HOST, ES_PORT

app = fastapi.FastAPI()

s = sessionmaker(bind=engine)
session = s()

es = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")

mappings = {
    "properties": {
        "id": {"type": "long"},
        "text": {"type": "text"}
    }
}

# es.indices.create(index="documents", mappings=mappings)


@app.get("/search/{text}")
def search_text(text: str):
    result = session.query(Documents).filter(Documents.text.like(f"%{text}%")).order_by(Documents.created_date.desc())
    return [doc for doc in result]


@app.get("/es-info")
def get_es_info():
    return es.info()


@app.get("/insert-test-data")
def insert_test_data():
    df = pandas.read_csv("posts.csv")
    for i, row in df.iterrows():
        doc = Documents(row["text"], row["created_date"], row["rubrics"])
        session.add(doc)
        session.flush()
        session.refresh(doc)

        doc = {
            "id": doc.id,
            "text": row["text"]
        }
        es.index(index="documents", id=i, document=doc)

    session.commit()


@app.get("/delete-all-data")
def delete_all_data():
    es.delete_by_query(index="documents", body={"query": {"match_all": {}}})
    session.query(Documents).delete()
    session.flush()
    session.commit()


@app.get("/get-count")
def get_count():
    return es.count(index="documents")


@app.get("/get-doc/{num}")
def get_doc(num: str):
    resp = es.get(index="documents", id=num)
    return resp


@app.get("/elastic-search/{doc_text}")
def elastic_search(doc_text: str):
    resp = es.search(
        index="documents",
        size=20,
        query={
            "term": {
                    "text": doc_text,
                },
        },
    )

    doc_ids = (int(hit["_source"]["id"]) for hit in resp['hits']['hits'])
    #return sorted([session.get(Documents, i) for i in doc_ids], key=lambda d: d['created_date'])
    return [session.get(Documents, i) for i in doc_ids]


@app.get("/delete-doc/{doc_id}")
def delete_doc(doc_id: int):
    pass
