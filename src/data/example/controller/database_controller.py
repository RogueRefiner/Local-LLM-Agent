from dataclasses import dataclass, field
import pandas as pd
from data.example.service.database_service import DatabaseService
from pathlib import Path


@dataclass
class DatabaseController:
    """
    The DatabaseController class provides a high-level interface for managing interactions with a database.
    It uses an instance of DatabaseService to perform the actual database operations.

    Attributes:
        database_service (DatabaseService): An instance of DatabaseService responsible for handling database operations.

    Methods:
        read_csv(self, filepath: Path, index_column: str) -> pd.DataFrame: Reads data from a CSV file and returns it as a pandas DataFrame.
        insert_data(self, df: pd.DataFrame) -> None: Inserts the provided pandas DataFrame into the database.
    """

    database_service: DatabaseService = field(default_factory=lambda: DatabaseService())

    def read_csv(self, filepath: Path, index_column: str) -> pd.DataFrame:
        """
        Reads data from a CSV file and returns it as a pandas DataFrame.

        Args:
            filepath (Path): The path to the CSV file.
            index_column (str): The name of the column to use as the index for the DataFrame.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data from the CSV file, with the specified column set as the index.
        """
        return pd.read_csv(filepath, index_col=index_column)

    def insert_data(self, df: pd.DataFrame) -> None:
        """
        Inserts the provided pandas DataFrame into the database.

        Args:
            df (pd.DataFrame): The pandas DataFrame to be inserted into the database.
        """
        self.database_service.insert_data(df)


def get_database_controller() -> DatabaseController:
    """
    Returns a new instance of DatabaseController.

    Returns:
        DatabaseController: A new instance of DatabaseController with default values for its attributes.
    """
    return DatabaseController()
