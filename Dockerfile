FROM python:3.9.6-slim-buster
RUN apt-get update -y
RUN apt-get install -y cron

# Prepping the runtime
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
CMD ./manage.py runserver 0.0.0.0:8000
