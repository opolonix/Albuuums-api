FROM python:3.11-slim

COPY ..

RUN pip install -r requirements.txt

CMD {"uvicorn", "main:app", "0.0.0.0", "--port", "7474"}