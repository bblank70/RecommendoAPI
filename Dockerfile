FROM python:3.10.11-slim-buster
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP = app.python
CMD ["flask", "run" "--host", "0.0.0.0"]

