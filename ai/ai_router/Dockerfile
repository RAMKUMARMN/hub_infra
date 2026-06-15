FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Environment variables will be injected via docker-compose

# Start the interactive simulator
CMD ["python", "-m", "app.main"]
