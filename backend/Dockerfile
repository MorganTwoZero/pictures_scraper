FROM python:slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1