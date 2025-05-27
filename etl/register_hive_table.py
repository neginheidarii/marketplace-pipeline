from pyspark.sql import SparkSession

# Start SparkSession with Hive support
spark = SparkSession.builder \
    .appName("RegisterHiveTable") \
    .config("spark.sql.catalogImplementation", "hive") \
    .config("hive.metastore.uris", "thrift://localhost:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Load Parquet data
df = spark.read.parquet("data/processed/listings.parquet")

# Create Hive table (if not exists) and insert data
df.write.mode("overwrite").saveAsTable("marketplace.listings")

print("✅ Hive table 'marketplace.listings' created and loaded!")
