FROM python:3.10-alpine as builder

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip/ pip install -r requirements.txt