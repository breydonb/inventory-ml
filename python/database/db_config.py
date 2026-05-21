import os
from dataclasses import dataclass

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    dbname: str

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        # Create a dictionary of required fields and their values from environment variables
        required_fields = {
            'DB_USER': os.getenv('DB_USER'),
            'DB_PASSWORD': os.getenv('DB_PASSWORD'),
            'DB_NAME': os.getenv('DB_NAME'),
            'DB_HOST': os.getenv('DB_HOST')
        }
        # create an array of missing fields by checking which required values are null or empty
        missing = [
            name
            for name, value in required_fields.items()
            if not value
        ]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
        
        port_raw = os.getenv("DB_PORT", "5432")
        try:
            port = int(port_raw)
        except ValueError as e:
            raise EnvironmentError(
                f"DB_PORT must be an integer, port type: {port_raw!r} "
            ) from e

        return cls(
            host=os.environ["DB_HOST"],
            port=port,
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            dbname=os.environ["DB_NAME"]
        )