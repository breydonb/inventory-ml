import csv

class CSVExporter:
    def __init__(self, conn):
        self.conn = conn

    def export_table_to_csv(self, function_name: str, output_file: str) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {function_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            writer.writerows(rows)

    def export_all_tables(self, output_directory: str) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            output_file = f"{output_directory}/{table_name}.csv"
            self.export_table_to_csv(table_name, output_file)