FROM python:3.11-slim

WORKDIR /app

# System deps for kaggle and unzip
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV OTAFP_DEBUG=true

EXPOSE 8000
CMD ["python", "main.py"]
