import psycopg2
import time
import os

import pandas as pd # pyright: ignore[reportMissingModuleSource]

from database.db_config import DatabaseConfig
from database.connection import DatabaseConnection
from database.tables import ALL_TABLES, CSV_IMPORTS
from database.manager import DatabaseManager
from database.csv_loader import CSVLoader
from database.sql_runner import SQLRunner
from database.csv_exporter import CSVExporter

def import_csv_to_db(conn: psycopg2.extensions.connection):
    directory = os.listdir("data/")
    for file in directory:
        if file.endsWith(".csv"):
            df = pd.read_csv(f"data/{file}")
            for index, row in df.iterrows():
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO inventory (item_id, item_name, quantity) VALUES (%s, %s, %s)",
                        (row['item_id'], row['item_name'], row['quantity'])
                    )
            conn.commit()

def connect_with_retry(
    conn: DatabaseConnection,
    max_attempts: int = 5,
    delay_seconds: int = 5
):
    for attempt in range(1, max_attempts + 1):
        try:
            return conn.connect()
        except RuntimeError as e:
            print(f"Database connection error: {e}")
            
            if attempt == max_attempts:
                raise

            print(
                f"Retrying in {delay_seconds} seconds..." 
                f"Attempt: {attempt} / {max_attempts}"
            )
            time.sleep(delay_seconds)
        raise RuntimeError("Failed to connect to database.")

def main() -> None:
    config = DatabaseConfig.from_env()
    db_connection = DatabaseConnection(config)

    try:
        conn = connect_with_retry(db_connection)
        
        manager = DatabaseManager(conn)
        manager.create_tables(ALL_TABLES)

        csv_loader = CSVLoader(conn)
        csv_loader.import_all()
        print("Database setup and CSV import completed successfully.")

        sql_runner = SQLRunner(conn)
        sql_runner.run_sql_functions("database/sql/functions")

        exporter = CSVExporter(conn)
        exporter.export_table_to_csv("get_unused_devices()", "data/CrowdstrikeInventoryInnerJoin.csv")
    except Exception as e:
        if conn is not None:
            conn.rollback()
        raise
    finally:
        db_connection.close()
    

if __name__ == "__main__":
    main()