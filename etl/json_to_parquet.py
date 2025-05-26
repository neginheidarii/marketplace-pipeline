from pyspark.sql import SparkSession


# Create a Spark session
spark = SparkSession.builder \
    .appName("Kijiji ETL") \
    .getOrCreate()

# Read the JSON file
df = spark.read.option("multiLine", True).json("data/raw/listings.json")
 
# Show schema and data 
df.printSchema()
df.show(truncate=False)

# Save as Parquet
df.write.mode("overwrite").parquet("data/processed/listings.parquet")
print("✅ Saved listings to data/processed/listings.parquet")


spark.stop()
