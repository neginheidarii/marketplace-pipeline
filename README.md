# 🛒 Marketplace Pipeline - README

This project builds a scalable data pipeline that crawls online marketplaces (like Kijiji), processes and stores the data using Apache Spark and Hive, and exposes it through a REST API built with FastAPI.

---

## 📦 Project Structure

```
marketplace-pipeline/
├── api/                    # FastAPI backend (main.py, hive_queries.py)
├── data/                   # Directory for raw and processed data (e.g., listings.parquet)
├── docker-compose.yml      # Multi-container Docker setup
├── Dockerfile              # FastAPI API Dockerfile
├── requirements.txt        # Python dependencies
├── venv/                   # Python virtual environment
```

---

## 🐳 Dockerized Services

The system uses Docker Compose to run multiple services:

| Service           | Description                                    |
| ----------------- | ---------------------------------------------- |
| `marketplace-api` | FastAPI backend with SparkSession              |
| `spark`           | Apache Spark Master (via Bitnami image)        |
| `hive-metastore`  | Hive Metastore backed by PostgreSQL            |
| `hive-server`     | HiveServer2 to allow querying Hive from PyHive |
| `postgres`        | Metadata store for Hive                        |

---

## ⚙️ Prerequisites

* Docker & Docker Compose
* Python 3.10+ (only for local development, not needed inside containers)
* Optional: VSCode with Python extensions

---

## 🚀 How to Run the System

### 1. **Start Docker Services**

```bash
docker-compose up --build
```

> This builds the FastAPI container and starts all services (Spark, Hive, etc.)

### 2. **API Access**

* Local API: [http://localhost:8000](http://localhost:8000)
* Docs UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. **Frontend Access (Optional)**

If you have a frontend in `frontend/`:

```bash
cd frontend
npm install
npm run dev
```

Then access: [http://localhost:3000](http://localhost:3000)

---

## 🔍 API Endpoints

| Endpoint                | Description                       |
| ----------------------- | --------------------------------- |
| `/`                     | Health check                      |
| `/listings/cheapest`    | Get top 10 cheapest listings      |
| `/listings/by-location` | Filter listings by city and price |
| `/hive/tables`          | Lists Hive tables via PyHive      |

---

## 📚 Notes on Hive Integration

To query Hive tables from FastAPI:

* Use `PyHive` package with SASL, Thrift, etc.
* Connect to `hive-server` at `localhost:10000`
* Setup in `api/hive_queries.py`

---

## 🐞 Troubleshooting

### Common Errors

| Error                                    | Cause                                     | Fix                              |
| ---------------------------------------- | ----------------------------------------- | -------------------------------- |
| `longintrepr.h not found`                | C++ header issue on macOS ARM64           | Use Docker to avoid local builds |
| `Could not resolve module ...` in VSCode | VSCode not using right Python interpreter | Switch to `venv310` in VSCode    |
| `Cannot connect to Docker daemon`        | Docker not running                        | Launch Docker Desktop            |

---

## ✍️ Contributing

To add new data sources, edit the crawler logic in a new script and ensure it outputs to `data/processed/` as a Parquet file.

To add new API logic, modify or extend `api/main.py`.

---

## 🧪 Test the Logic (in container)

1. **Open a terminal inside the container:**

```bash
docker exec -it marketplace-api /bin/bash
```

2. **Run Python and test Spark logic:**

```bash
python
>>> from pyspark.sql import SparkSession
>>> spark = SparkSession.builder.master("spark://spark:7077").appName("Test").getOrCreate()
>>> df = spark.read.parquet("data/processed/listings.parquet")
>>> df.show()
```

---

## 📄 License

MIT License (2025)
