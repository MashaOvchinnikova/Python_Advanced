FROM python:3.10.6-alpine

LABEL authors="mashaovchinnikova"

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN python -m pip install -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["python", "app.py"]