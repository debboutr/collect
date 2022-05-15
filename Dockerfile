FROM python:3.9-slim-buster
ENV TZ="America/Los_Angeles"
WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "wsgi:app"]
