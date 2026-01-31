from dataclasses import dataclass, field
from typing import Any
from dotenv import load_dotenv
import os
from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine, inspect, text
from sqlalchemy.engine.base import Engine
from data.example.database.models import Base
from utils.logger.app_logger import ApplicationLogger


@dataclass
class DatabaseManager:
    """
    Manages the database connection and ensures that all expected tables are created.

    Attributes:
        database (str): The name of the database.
        username (str): The username for accessing the database.
        password (str): The password for accessing the database.
        host (str): The host where the database server is running.
        port (str): The port on which the database server is listening.
        dialect (str): The SQL dialect used by the database.
        driver (str): The database driver to use.
        database_logger (ApplicationLogger, optional): Logger for database-related activities. Defaults to a new `ApplicationLogger`.
        engine (Engine): The SQLAlchemy engine object used for connecting to and managing the database.

    Methods:
        __post_init__(): Initializes the database connection and verifies that all expected tables are created.
        insert(self, table_name: str, data: list[dict[str, Any]]) -> None | list[int]:
    """

    database: str
    username: str
    password: str
    host: str
    port: str
    dialect: str
    driver: str
    metadata: MetaData = field(default_factory=lambda: MetaData())
    database_logger: ApplicationLogger = field(
        default_factory=lambda: ApplicationLogger()
    )
    engine: Engine = field(init=False)

    def __post_init__(self) -> None:
        """
        Initializes the database connection and verifies that all expected tables are created.

        This method is called automatically after the instance of the class has been initialized.
        It sets up the database engine using the provided credentials and dialect, creates all tables
        defined in the Base metadata, and checks if the correct number of tables have been created.

        Raises:
            Exception: If an error occurs during the initialization process, including issues with creating
                    the database engine or verifying table creation.
        """
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

    def insert_dimension_tables(
        self, table_name: str, column_name: str, data: list[dict[str, Any]]
    ) -> None | dict[str, int]:
        """
        Inserts data into a specified database table.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            data (list[dict[str, Any]]): A list of dictionaries where each dictionary represents a row of data to be inserted.

        Returns:
            None or list[int]: If successful, returns a list of IDs for the inserted rows. Otherwise, returns None.
        """
        inspector = inspect(self.engine)

        if not inspector.has_table(table_name):
            self.database_logger.error(f"Table does not exist: {table_name}")
            return

        table = Table(table_name, self.metadata, autoload_with=self.engine)
        statement = table.insert().returning(table.c.id)

        with self.engine.begin() as connection:
            result = connection.execute(statement, data)
            values = [d[column_name].lower() for d in data]
            ids = list(result.scalars().all())
            self.database_logger.debug(f"values: {values}\nids: {ids}")
            id_to_value_dict = dict(zip(values, ids))
            self.database_logger.debug(f"id_to_value_dict: {id_to_value_dict}")

            self.database_logger.debug(f"Inserted Rows: {result.rowcount}")

        return id_to_value_dict

    def insert_fact_table(self, table_name: str, data: DataFrame) -> None:
        """
        Inserts data into a fact table.
        Args:

            table_name (str): The name of the table.
            data (DataFrame): The data to insert.
        """
        with self.engine.begin() as connection:
            data.to_sql(table_name, connection, index=False, if_exists="append")


def load_db_config() -> DatabaseManager:
    """
    Loads database configuration from environment variables and creates a `DatabaseManager` instance with the provided parameters.

    Returns:
        DatabaseManager: A `DatabaseManager` object configured with the database details.
    """
    load_dotenv()
    database = os.getenv("EXAMPLE_DATABASE", "example_database")
    username = os.getenv("EXAMPLE_USERNAME", "username")
    password = os.getenv("EXAMPLE_PASSWORD", "password")
    host = os.getenv("EXAMPLE_HOST", "localhost")
    port = os.getenv("EXAMPLE_PORT", "1234")
    dialect = os.getenv("EXAMPLE_DIALECT", "postgresql")
    driver = os.getenv("EXAMPLE_DRIVER", "psycopg2")

    return DatabaseManager(database, username, password, host, port, dialect, driver)
