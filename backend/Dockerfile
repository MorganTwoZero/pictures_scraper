FROM python:slim

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY / .