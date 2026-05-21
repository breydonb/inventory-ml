import pandas as pd # pyright: ignore[reportMissingModuleSource]
from pathlib import Path

from psycopg2 import sql
from psycopg2.extensions import connection as PsycopgConnection

from database.schema import Table, Column
from database.tables import CSV_IMPORTS, INVENTORY_TABLE

class CSVLoader:
    def __init__(self, connection: PsycopgConnection):
        self.connection = connection

    def import_all(self) -> None:
        for table, file_path in CSV_IMPORTS:
            self._import_csv(table, file_path)
    def _import_csv(self, table: Table, file_path: str) -> None:
        df = self._load_csv(file_path)
        df = self._shape_dataframe(df, table)
        self._insert_dataframe(table, df)

    def _load_csv(self, file_path: str) -> pd.DataFrame:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        return pd.read_csv(file_path, encoding="utf-8-sig")
    
    def _get_import_columns(self, table: Table) -> list[str]:
        return [
            column
            for column in table.columns
            if column.csv_name is not None
        ]
    
    def _shape_dataframe(self, df: pd.DataFrame, table: Table) -> pd.DataFrame:
        df.columns = df.columns.astype(str).str.strip()
        
        import_columns = self._get_import_columns(table)

        expected_csv_columns = [
            column.csv_name
            for column in import_columns
        ]

        missing_csv_columns = [
            column_name
            for column_name in expected_csv_columns
            if column_name not in df.columns
        ]

        if missing_csv_columns:
            raise ValueError(
                f"Missing columns in CSV for table '{table.name}': {missing_csv_columns}"
            )
        
        df = df[expected_csv_columns]

        rename_map = {
            column.csv_name: column.name
            for column in import_columns
        }

        df = df.rename(columns=rename_map)
        
        expected_db_columns = [
            column.name
            for column in import_columns
        ]

        df = df[expected_db_columns]

        for column in import_columns:
            df[column.name] = df[column.name].apply(
                lambda x: self._convert_value(
                    data_type=column.data_type,
                    value=x,
                    column_name=column.name
                )
            )
        return df
    def _insert_dataframe(self, table: Table, df: pd.DataFrame) -> None:
        import_columns = self._get_import_columns(table)

        columns = [
            column.name
            for column in import_columns
        ]

        insert_query = sql.SQL("""
            INSERT INTO {table} ({fields})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING
        """).format(
            table=sql.Identifier(table.name),
            fields=sql.SQL(', ').join(
                sql.Identifier(column) for column in columns
            ),
            placeholders=sql.SQL(', ').join(
                sql.Placeholder() for _ in columns
            )
        )
        rows = list(df.itertuples(index=False, name=None))

        with self.connection.cursor() as cursor:
            cursor.executemany(insert_query, rows)
        self.connection.commit()
    
    def _convert_value(self, data_type, value, column_name: str):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            value = value.strip()
        if value == "":
            return None
        normalize_type = data_type.upper()
        try:
            if normalize_type.startswith("VARCHAR"):
                return str(value)
            elif normalize_type == "INTEGER":
                return int(value)
            elif normalize_type == "DATE":
                return self._convert_date(value)
            elif normalize_type == "TIMESTAMP":
                return self._convert_timestamp(value)
            elif normalize_type == "TEXT":
                return str(value)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
        except Exception as e:
            raise ValueError(
                f"Failed to convert {column_name} with value '{value}' to type '{data_type}'"
            ) from e
        
    def _convert_date(self, value) -> pd.Timestamp | None:
        cleaned = str(value).strip()
        if cleaned.upper() in {"NEW", "UNKNOWN", "N/A", "NA", ""}:
            return None
        return pd.to_datetime(cleaned, errors="raise").date()
    
    def _convert_timestamp(self, value) -> pd.Timestamp | None:
        cleaned = str(value).strip()
        if cleaned.upper() in {"NEW", "UNKNOWN", "N/A", "NA", ""}:
            return None
        return pd.to_datetime(cleaned, errors="raise").to_pydatetime()