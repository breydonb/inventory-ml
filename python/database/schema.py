from dataclasses import dataclass, field
from psycopg2 import sql

@dataclass(frozen=True)
class Column:
    name: str
    data_type: str
    csv_name: str | None = None
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: str | None = None
    

    def build_query(self) -> sql.Composed:
        parts = [sql.SQL(self.data_type)]
        if self.default is not None:
            parts.extend([sql.SQL("DEFAULT"), sql.SQL(self.default)])
        if not self.nullable:
            parts.append(sql.SQL("NOT NULL"))
        if self.primary_key:
            parts.append(sql.SQL("PRIMARY KEY"))
        if self.unique:
            parts.append(sql.SQL("UNIQUE"))
        return sql.SQL(" ").join(parts)
    
@dataclass(frozen=True)
class Table:
    name: str
    columns: list[Column]

    def create_table_sql(self) -> sql.Composed:
        column_definitions = [
            sql.SQL("{} {}").format(
                sql.Identifier(column.name),
                column.build_query()
            )
            for column in self.columns
        ]
        return sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(self.name),
            sql.SQL(", ").join(column_definitions)
        )