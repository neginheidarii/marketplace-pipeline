FROM python:3.9-slim

WORKDIR /app

# Install system-level build dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libsasl2-dev \
    gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose port
EXPOSE 8000

# Start the FastAPI app
CMD ["tail", "-f", "/dev/null"]
