from pyhive import hive

def get_table_names():
    try:
        conn = hive.Connection(host="hive-server", port=10000, username="hive")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        return {"error": str(e)}
