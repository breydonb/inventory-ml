from pathlib import Path
from psycopg2.extensions import connection as PsycopgConnection

class SQLRunner:
    def __init__(self, connection: PsycopgConnection):
        self.connection = connection

    def run_sql_file(self, file_path: str) -> None:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")
        
        with file_path.open("r", encoding="utf-8") as f:
            sql_content = f.read()
        
        with self.connection.cursor() as cursor:
            cursor.execute(sql_content)
        self.connection.commit()
    
    def run_sql_functions(self, dir: str | Path) -> None:
        dir = Path(dir)
        if not dir.exists() or not dir.is_dir():
            raise FileNotFoundError(f"SQL functions directory not found: {dir}")
        
        sql_files = sorted(dir.glob("*.sql"))
        for sql_file in sql_files:
            self.run_sql_file(sql_file)