FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update && \
    apt-get install --reinstall -y libexpat1 && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install -r requirements.txt