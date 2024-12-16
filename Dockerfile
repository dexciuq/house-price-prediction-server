FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
