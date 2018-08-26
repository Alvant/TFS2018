FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/code

RUN pip install Django
RUN pip install psycopg2

COPY . /opt/code/
