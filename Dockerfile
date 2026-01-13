FROM python:3.12-slim

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.Main:app", "--host", "0.0.0.0", "--port", "8000"]