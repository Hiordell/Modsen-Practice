FROM python:3.11.4-alpine3.18
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk update && \
    apk add curl && \
    apk add mariadb-dev mariadb-client musl-dev mariadb-connector-c mysql gcc g++
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

ENTRYPOINT [ "/bin/sh", "/code/app.sh" ]