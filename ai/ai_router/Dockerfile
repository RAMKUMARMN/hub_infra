FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Environment variables will be injected via docker-compose

EXPOSE 8003

# Start the FastAPI web service
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8003"]
