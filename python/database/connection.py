import psycopg2
from psycopg2.extensions import connection as PsycopgConnection
from psycopg2 import OperationalError

from .db_config import DatabaseConfig

class DatabaseConnection:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self.connection: PsycopgConnection | None = None

    def connect(self) -> PsycopgConnection:
        if self.connection is None or self.connection.closed:
            try:
                self.connection = psycopg2.connect(
                    host=self.config.host,
                    port=self.config.port,
                    user=self.config.user,
                    password=self.config.password,
                    dbname=self.config.dbname
                )
            except OperationalError as e:
                raise RuntimeError(
                    f"Failed to connect to the database: '{self.config.dbname}' "
                    f"at {self.config.host}:{self.config.port} "
                    f"with user '{self.config.user}'"
                ) from e
        return self.connection
        
    def close(self) -> None:
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.connection = None