FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python core/tables.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7272"]