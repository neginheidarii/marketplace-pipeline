from fastapi import FastAPI
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import json
import os
from fastapi import Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from api.hive_queries import get_hive_data



app = FastAPI()


# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join("api", "static", "favicon.ico"))


# Initialize Spark session once (not per request)
spark = SparkSession.builder.appName("Marketplace API").getOrCreate()

@app.get("/")
def read_root():
    return {"message": "Marketplace API is running!"}

@app.get("/listings/cheapest")
def get_cheapest():
    df = spark.read.parquet("data/processed/listings.parquet")
    df = df.withColumn("price_num", expr("try_cast(price AS double)"))
    df = df.filter("price_num IS NOT NULL")
    df = df.orderBy("price_num").select("title", "price_num", "location", "url")
    listings = df.limit(10).toJSON().map(lambda j: json.loads(j)).collect()
    return {"results": listings}
 

from fastapi import Query

@app.get("/listings/by-location")
def get_listings_by_location(
    location: str = Query(..., description="e.g., City of Toronto"),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    df = spark.read.parquet("data/processed/listings.parquet")
    df = df.withColumn("price_num", expr("try_cast(price AS double)"))
    df = df.filter("price_num IS NOT NULL")
    df = df.filter(df.location == location)

    # Optional price filters
    if min_price is not None:
        df = df.filter(df.price_num >= min_price)
    if max_price is not None:
        df = df.filter(df.price_num <= max_price)

    df = df.orderBy("price_num")
    listings = df.select("title", "price_num", "location", "url").limit(20).toJSON().map(lambda j: json.loads(j)).collect()
    return {"results": listings}


@app.get("/hive/tables")
def list_hive_tables():
    return {"tables": get_hive_data()}