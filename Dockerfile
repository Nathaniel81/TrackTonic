FROM python:3.11.4-slim-bullseye
ENV PYTHONUNBUFFERED=1

WORKDIR /Django

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000