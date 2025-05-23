# Use an official Python image with Java for Spark
FROM openjdk:17-slim

# Set work directory
WORKDIR /app

# Install pip and required system packages
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv && \
    apt-get clean

# Copy requirements file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
