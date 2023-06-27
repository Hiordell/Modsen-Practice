from elasticsearch import Elasticsearch

from config import ES_HOST, ES_PORT

es = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")

mappings = {
    "properties": {
        "id": {"type": "long"},
        "text": {"type": "text"}
    }
}

es.indices.create(index="documents", mappings=mappings)
