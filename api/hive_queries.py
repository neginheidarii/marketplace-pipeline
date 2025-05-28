from pyhive import hive
from TCLIService.ttypes import TOperationState
import os

def get_hive_data():
    try:
        # Connect to Hive using environment variable or default values
        conn = hive.Connection(
            host=os.getenv("HIVE_HOST", "hive-server"),
            port=int(os.getenv("HIVE_PORT", 10000)),
            username=os.getenv("HIVE_USER", "hive"),
            database=os.getenv("HIVE_DATABASE", "default")
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables

    except Exception as e:
        return {"error": str(e)}
