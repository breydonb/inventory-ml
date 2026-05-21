from psycopg2.extensions import connection as PsycopgConnection
from database.schema import Table

class DatabaseManager:
    def __init__(self, connection: PsycopgConnection) -> None:
        self.connection = connection

    def __create_table(self, table: Table) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(table.create_table_sql())
        
    def create_tables(self, tables: list[Table]) -> None:
        for table in tables:
            self.__create_table(table)
        self.connection.commit()
        
