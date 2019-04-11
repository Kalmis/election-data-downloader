FROM python:3-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY src/ /app
WORKDIR /app

RUN mkdir /data

CMD ["python", "-u", "main.py"]
