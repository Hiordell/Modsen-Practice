#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "Postgres started"
fi

alembic upgrade head

if [ "$ES_DATABASE" = "elasticsearch" ]; then
    echo "Waiting for elastic..."

    while ! curl -s $ES_HOST:$ES_PORT >/dev/null; do
        sleep 1
    done

    echo "Elastic started"
fi

python index.py

uvicorn main:app --reload --host 0.0.0.0 --port 8000
