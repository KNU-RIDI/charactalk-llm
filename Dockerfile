FROM python:3.13.2-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

ENV PYTHONUNBUFFERED 1

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
