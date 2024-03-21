FROM python:3.11-slim

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/core

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7272"]