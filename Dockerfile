FROM openjdk:17-slim

# Install Python, pip, and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && apt-get clean

# Install Spark (you can change the version if needed)
ENV SPARK_VERSION=3.5.1
RUN curl -fSL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz" \
    -o /tmp/spark.tgz \
 && tar -xzf /tmp/spark.tgz -C /opt/ \
 && rm /tmp/spark.tgz
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH



# Set environment variable to access Hive Metastore
ENV HIVE_METASTORE_URI=thrift://hive-metastore:9083

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Set PYSPARK-related environment vars
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
