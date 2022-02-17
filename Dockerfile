FROM python:3.9-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD ["python3", "app.py"]
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "wsgi:app"]
