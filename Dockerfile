FROM python:3.13.2-slim

WORKDIR /app

COPY . /app

EXPOSE $PORT

ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
