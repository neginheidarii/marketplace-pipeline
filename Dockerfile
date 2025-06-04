FROM python:3.9-slim

WORKDIR /app

# Install Java and system-level build tools
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3-dev \
    build-essential \
    libsasl2-dev \
    gcc \
    && apt-get clean

# Set JAVA_HOME for PySpark to find Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Expose port
EXPOSE 8000

# Keep container running for debugging
CMD ["tail", "-f", "/dev/null"]
