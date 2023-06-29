FROM python:3.11.4-alpine3.18
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk update && \
    apk add curl
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

ENTRYPOINT [ "/bin/sh", "/code/app.sh" ]