FROM python:3.9-slim

WORKDIR /app

# Install system-level build dependencies including Java
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3-dev \
    build-essential \
    libsasl2-dev \
    gcc \
    && apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project code
COPY . .

# Default command
CMD ["tail", "-f", "/dev/null"]
