FROM python:3.10.11-alpine

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt
COPY ./app.py /app/
COPY ./response.json /app/



CMD ["flask", "run", "--host", "0.0.0.0"]

