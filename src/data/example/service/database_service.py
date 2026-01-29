from dataclasses import dataclass, field
from utils.logger.app_logger import ApplicationLogger
from data.example.database.database_manager import DatabaseManager, load_db_config
import pandas as pd
from data.example.utils.EAcademicLevel import EAcademicLevel
from data.example.utils.EGender import EGender
from data.example.utils.EPlatform import EPlatform
from data.example.utils.ERelationshipStatus import ERelationshipStatus
import numpy as np


@dataclass
class DatabaseService:
    """
    A class providing services for interacting with a database, including inserting various types of data.

    This class manages interactions with a database through an instance of `DatabaseManager` and logs its activities using an instance of `ApplicationLogger`.

    Attributes:
        logger (ApplicationLogger): An instance of `ApplicationLogger` for logging database operations.
        database_manager (DatabaseManager): An instance of `DatabaseManager` for managing database interactions.

    Methods:
        - insert_data(df: pd.DataFrame) -> None: Inserts data from a DataFrame into the database.
        - __insert_genders(table_name: str, genders: np.ndarray) -> None | list[int]: Inserts gender data into the specified table.
        - __insert_academic_levels(table_name: str, academic_levels: np.ndarray) -> None | list[int]: Inserts academic level data into the database.
        - __insert_countries(table_name: str, countries: np.ndarray) -> None | list[int]: Inserts country data into the database.
        - __insert_platforms(table_name: str, platforms: np.ndarray) -> None | list[int]: Inserts platform data into the database.
        - __insert_students(table_name: str, df: pd.DataFrame) -> None: Inserts student data from a DataFrame into the database.
    """

    logger: ApplicationLogger = field(default_factory=lambda: ApplicationLogger())
    database_manager: DatabaseManager = field(default_factory=lambda: load_db_config())

    def insert_data(self, df: pd.DataFrame) -> None:
        """
        Inserts data from a DataFrame into the database.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be inserted.
        """
        gender_ids = self.__insert_genders("genders", "gender", df["Gender"].unique())
        self.logger.debug(f"gender_ids: {gender_ids}")
        academic_level_ids = self.__insert_academic_levels(
            "academic_levels", "academic_level", df["Academic_Level"].unique()
        )
        self.logger.debug(f"academic_level_ids: {academic_level_ids}")
        country_ids = self.__insert_countries(
            "countries", "country_name", df["Country"].unique()
        )
        self.logger.debug(f"country_ids: {country_ids}")
        platform_ids = self.__insert_platforms(
            "platforms", "platform", df["Most_Used_Platform"].unique()
        )
        self.logger.debug(f"platform_ids: {platform_ids}")

    def __insert_genders(
        self, table_name: str, column_name: str, genders: np.ndarray
    ) -> None | dict[int, str]:
        """
        Inserts gender data into the specified table.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            genders (np.ndarray): An array containing unique gender values.

        Returns:
            None or dict[int, str]: If successful, returns a dict mapping the inserted ids to the values. Otherwise, returns None.
        """
        data = [{column_name: EGender(gender.upper()).value} for gender in genders]
        self.logger.debug(f"data: {data}")
        gender_ids = self.database_manager.insert(table_name, column_name, data)

        return gender_ids

    def __insert_academic_levels(
        self, table_name: str, column_name: str, academic_levels: np.ndarray
    ) -> None | dict[int, str]:
        """
        Inserts academic level data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            academic_levels (np.ndarray): An array containing unique academic level values.

        Returns:
            None or dict[int, str]: If successful, returns a dict mapping the inserted ids to the values. Otherwise, returns None.
        """
        data = [
            {column_name: EAcademicLevel(academic_level.upper()).name}
            for academic_level in academic_levels
        ]
        self.logger.debug(f"data: {data}")
        academic_level_ids = self.database_manager.insert(table_name, column_name, data)

        return academic_level_ids

    def __insert_countries(
        self, table_name: str, column_name: str, countries: np.ndarray
    ) -> None | dict[int, str]:
        """
        Inserts country data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            countries (np.ndarray): An array containing unique country values.

        Returns:
            None or dict[int, str]: If successful, returns a dict mapping the inserted ids to the values. Otherwise, returns None.
        """
        data = [{"country_name": country} for country in countries]
        self.logger.debug(f"data: {data}")
        country_ids = self.database_manager.insert(table_name, column_name, data)

        return country_ids

    def __insert_platforms(
        self, table_name: str, column_name: str, platforms: np.ndarray
    ) -> None | dict[int, str]:
        """
        Inserts platform data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            platforms (np.ndarray): An array containing unique platform values.

        Returns:
            None or dict[int, str]: If successful, returns a dict mapping the inserted ids to the values. Otherwise, returns None.
        """
        data = [{column_name: EPlatform(platform.upper())} for platform in platforms]
        self.logger.debug(f"data: {data}")
        platform_ids = self.database_manager.insert(table_name, column_name, data)

        return platform_ids

    def __insert_students(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Inserts student data from a DataFrame into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            df (pd.DataFrame): The DataFrame containing the student data to be inserted.
        """
        pass
