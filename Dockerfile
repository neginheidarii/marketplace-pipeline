FROM openjdk:17-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/local/openjdk-17
ENV SPARK_VERSION=3.5.1

# Install Python and required tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    procps \
    && apt-get clean

# Install Spark
RUN curl -fSL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz" \
    -o /tmp/spark.tgz \
 && tar -xzf /tmp/spark.tgz -C /opt/ \
 && rm /tmp/spark.tgz
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH

# Set Hive Metastore URI (if needed)
ENV HIVE_METASTORE_URI=thrift://hive-metastore:9083

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
