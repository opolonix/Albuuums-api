FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD {"uvicorn", "main:app", "0.0.0.0", "--port", "80"}