from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# 1. Start Spark session
spark = SparkSession.builder.appName("Query Listings").getOrCreate()

# 2. Load the Parquet file
df = spark.read.parquet("data/processed/listings.parquet")
 
# 3. Listings per location
print("📍 Listings per location:")
df.groupBy("location").count().orderBy("count", ascending=False).show(truncate=False)

# 4. Safely cast price using try_cast (Spark 3.5+ safe method)
df_clean = df.withColumn("price_num", expr("try_cast(price AS double)"))

# 5. Filter out rows where casting failed (price_num is null)
df_filtered = df_clean.filter("price_num IS NOT NULL")

# 6. Show 10 cheapest items
print("💸 Top 10 cheapest (numeric only):")
df_filtered.orderBy("price_num").select("title", "price_num", "location").show(10, truncate=False)

# 7. Stop Spark
spark.stop()
