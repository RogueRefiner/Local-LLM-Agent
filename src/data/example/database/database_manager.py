from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine
from data.example.database.models import Base
from utils.logger.app_logger import ApplicationLogger


@dataclass
class DatabaseManager:
    database: str
    username: str
    password: str
    host: str
    port: str
    dialect: str
    driver: str
    database_logger: ApplicationLogger = field(
        default_factory=lambda: ApplicationLogger()
    )
    engine: Engine = field(init=False)

    def __post_init__(self) -> None:
        try:
            self.engine = create_engine(
                f"{self.dialect}+{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            Base.metadata.create_all(self.engine)
            with self.engine.connect() as connection:
                created_tables = connection.execute(
                    text(
                        "select * from pg_catalog.pg_tables WHERE schemaname = 'public'"
                    )
                )
                assert len(Base.metadata.tables) == len(
                    created_tables.all()
                ), "Error when generating tables"
        except Exception as e:
            self.database_logger.error(f"Error when initializing DatabaseManager: {e}")


def load_db_config() -> DatabaseManager:
    load_dotenv()
    database = os.getenv("EXAMPLE_DATABASE", "example_database")
    username = os.getenv("EXAMPLE_USERNAME", "username")
    password = os.getenv("EXAMPLE_PASSWORD", "password")
    host = os.getenv("EXAMPLE_HOST", "localhost")
    port = os.getenv("EXAMPLE_PORT", "1234")
    dialect = os.getenv("EXAMPLE_DIALECT", "postgresql")
    driver = os.getenv("EXAMPLE_DRIVER", "psycopg2")

    return DatabaseManager(database, username, password, host, port, dialect, driver)
