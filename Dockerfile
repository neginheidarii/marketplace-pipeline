FROM python:3.9-slim

WORKDIR /app

# Install system-level build dependencies and Java
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libsasl2-dev \
    gcc \
    default-jdk \
    && apt-get clean

# Set JAVA_HOME environment variable for PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose port
EXPOSE 8000

# Keep the container running (for manual debugging or script running)
CMD ["tail", "-f", "/dev/null"]
