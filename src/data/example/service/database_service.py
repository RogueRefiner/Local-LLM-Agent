from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Sequence

from sqlalchemy import RowMapping, Select, Sequence, and_, select, func
from data.example.database.models import (
    AcademicLevel,
    Country,
    Gender,
    Platform,
    Student,
)
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

        self.__insert_students(
            "students", df, gender_ids, academic_level_ids, country_ids, platform_ids
        )
        self.logger.debug(f"students successfully inserted")

    def __insert_genders(
        self, table_name: str, column_name: str, genders: np.ndarray
    ) -> None | dict[str, int]:
        """
        Inserts gender data into the specified table.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            genders (np.ndarray): An array containing unique gender values.

        Returns:
            None or dict[str, int]: If successful, returns a dict mapping the inserted values to the ids. Otherwise, returns None.
        """
        data = [{column_name: EGender(gender.upper()).value} for gender in genders]
        self.logger.debug(f"data: {data}")
        gender_ids = self.database_manager.insert_dimension_tables(
            table_name, column_name, data
        )

        return gender_ids

    def __insert_academic_levels(
        self, table_name: str, column_name: str, academic_levels: np.ndarray
    ) -> None | dict[str, int]:
        """
        Inserts academic level data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            academic_levels (np.ndarray): An array containing unique academic level values.

        Returns:
            None or dict[str, int]: If successful, returns a dict mapping the inserted values to the ids. Otherwise, returns None.
        """
        data = [
            {column_name: EAcademicLevel(academic_level.upper()).name}
            for academic_level in academic_levels
        ]
        self.logger.debug(f"data: {data}")
        academic_level_ids = self.database_manager.insert_dimension_tables(
            table_name, column_name, data
        )

        return academic_level_ids

    def __insert_countries(
        self, table_name: str, column_name: str, countries: np.ndarray
    ) -> None | dict[str, int]:
        """
        Inserts country data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            countries (np.ndarray): An array containing unique country values.

        Returns:
            None or dict[str, int]: If successful, returns a dict mapping the inserted values to the ids. Otherwise, returns None.
        """
        data = [{"country_name": country} for country in countries]
        self.logger.debug(f"data: {data}")
        country_ids = self.database_manager.insert_dimension_tables(
            table_name, column_name, data
        )

        return country_ids

    def __insert_platforms(
        self, table_name: str, column_name: str, platforms: np.ndarray
    ) -> None | dict[str, int]:
        """
        Inserts platform data into the database.

        Args:
            table_name (str): The name of the table to insert data into.
            column_name (str): The name of the column later used as foreign key.
            platforms (np.ndarray): An array containing unique platform values.

        Returns:
            None or dict[str, int]: If successful, returns a dict mapping the inserted values to the ids. Otherwise, returns None.
        """
        data = [{column_name: EPlatform(platform.upper())} for platform in platforms]
        self.logger.debug(f"data: {data}")
        platform_ids = self.database_manager.insert_dimension_tables(
            table_name, column_name, data
        )

        return platform_ids

    def __insert_students(
        self,
        table_name: str,
        df: pd.DataFrame,
        gender_ids: None | dict[str, int],
        academic_level_ids: None | dict[str, int],
        country_ids: None | dict[str, int],
        platform_ids: None | dict[str, int],
    ) -> None:
        """
        Inserts students data into the database.

        Args:
            table_name (str): The name of the table.
            df (pd.DataFrame): The DataFrame containing student data.
            gender_ids (dict[str, int]): A dictionary mapping gender strings to IDs.
            academic_level_ids (dict[str, int]): A dictionary mapping academic level strings to IDs.
            country_ids (dict[str, int]): A dictionary mapping country strings to IDs.
            platform_ids (dict[str, int]): A dictionary mapping platform strings to IDs.
        """
        df = self.__prepare_foreign_keys(
            df, gender_ids, academic_level_ids, country_ids, platform_ids
        )
        df = self.__prepare_relationship_status(df, "Relationship_Status")
        df = self.__prepare_column_names(df)
        self.database_manager.insert_fact_table(table_name, df)

    def __prepare_foreign_keys(
        self,
        df: pd.DataFrame,
        gender_ids: None | dict[str, int],
        academic_level_ids: None | dict[str, int],
        country_ids: None | dict[str, int],
        platform_ids: None | dict[str, int],
    ) -> pd.DataFrame:
        """
        Prepares foreign keys for the DataFrame based on the provided dictionaries.

        Args:
            df (pd.DataFrame): The DataFrame to prepare.
            gender_ids (dict[str, int]): A dictionary mapping gender strings to IDs.
            academic_level_ids (dict[str, int]): A dictionary mapping academic level strings to IDs.
            country_ids (dict[str, int]): A dictionary mapping country strings to IDs.
            platform_ids (dict[str, int]): A dictionary mapping platform strings to IDs.

        Returns:
            pd.DataFrame: The prepared DataFrame with foreign keys added.
        """
        if gender_ids and academic_level_ids and country_ids and platform_ids:
            df["gender_id"] = [gender_ids[str_val.lower()] for str_val in df["Gender"]]
            df["country_id"] = [
                country_ids[str_val.lower()] for str_val in df["Country"]
            ]
            df["platform_id"] = [
                platform_ids[str_val.lower()] for str_val in df["Most_Used_Platform"]
            ]
            df["academic_level_id"] = [
                (
                    academic_level_ids[str_val.lower()]
                    if str_val.count(" ") < 1
                    else academic_level_ids[str_val.replace(" ", "_").lower()]
                )
                for str_val in df["Academic_Level"]
            ]
        return df

    def __prepare_relationship_status(
        self, df: pd.DataFrame, column_name: str
    ) -> pd.DataFrame:
        """
        Prepares the relationship status column in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to prepare.
            column_name (str): The name of the column containing relationship statuses.

        Returns:
            pd.DataFrame: The prepared DataFrame with relationship status names converted to uppercase and renamed.
        """
        df[column_name] = [
            ERelationshipStatus(relationship_status.upper()).name
            for relationship_status in df[column_name]
        ]
        return df

    def __prepare_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepares the column names for the DataFrame by converting them to lowercase and dropping unnecessary columns.

        Args:
            df (pd.DataFrame): The DataFrame to prepare.

        Returns:
            pd.DataFrame: The prepared DataFrame with lowercased column names and dropped unnecessary columns.
        """
        df = df.drop(
            columns=["Gender", "Country", "Most_Used_Platform", "Academic_Level"]
        )
        columns = {column: column.lower() for column in df.columns}
        df.rename(columns=columns, inplace=True)
        return df

    def fetch_by_gender_and_academic_level(
        self, gender: EGender, academic_level: EAcademicLevel
    ) -> list[dict[Any, Any]]:
        """
        Fetch students based on gender and academic level.

        Args:
            gender (EGender): The gender of the students.
            academic_level (EAcademicLevel): The academic level of the students.

        Returns:
            list[dict[Any, Any]]: List of dictionaries representing the fetched students.
        """
        with self.database_manager.engine.begin() as connection:
            query = (self.__get_base_student_query()).where(
                and_(
                    Gender.gender == gender,
                    AcademicLevel.academic_level == academic_level,
                )
            )

            self.logger.debug(
                f"Executing query for gender={gender}, academic_level={academic_level}"
            )
            results = connection.execute(query).mappings().all()

        return [dict(result) for result in results]

    def fetch_avg_daily_usage_for_country(self, country: str) -> Decimal | None:
        """
        Fetch average daily usage for a specific country.

        Args:
            country (str): The name of the country.

        Returns:
            Decimal | None: The average daily usage hours or None if no results found.
        """
        with self.database_manager.engine.begin() as connection:
            query = (
                select(func.avg(Student.avg_daily_usage_hours))
                .join(Country, Student.country_id == Country.id)
                .where(Country.country_name == country)
            )
            self.logger.debug(f"Executing query for country: {country}")
            result = connection.execute(query).fetchone()
            value: Decimal | None = result[0] if result else None
        return value

    def fetch_conflicts_over_threshold(self, threshold: int) -> list[dict[Any, Any]]:
        """
        Fetch conflicts over a given threshold.

        Args:
            threshold (int): The conflict threshold.

        Returns:
            list[dict[Any, Any]]: List of dictionaries representing students with conflicts over the threshold.
        """
        with self.database_manager.engine.begin() as connection:
            query = self.__get_base_student_query().where(
                Student.conflicts_over_social_media > threshold
            )
            self.logger.debug(f"Executing query for threshold: {threshold}")
            results = connection.execute(query).mappings().all()

        return [dict(result) for result in results]

    def fetch_students_by_affected_flag(
        self, is_affected: bool
    ) -> list[dict[Any, Any]]:
        """
        Fetch students by their affected flag.

        Args:
            is_affected (bool): Whether the student affects academic performance or not.

        Returns:
            list[dict[Any, Any]]: List of dictionaries representing affected students.
        """
        with self.database_manager.engine.begin() as connection:
            query = self.__get_base_student_query().where(
                Student.affects_academic_performance == is_affected
            )
            self.logger.debug(f"Executing query for is_affected: {is_affected}")
            results = connection.execute(query).mappings().all()
        return [dict(result) for result in results]

    def fetch_students_by_country_and_mental_health(
        self, country: str, mental_health: int
    ) -> list[dict[Any, Any]]:
        """
        Fetch students based on country and mental health score.

        Args:
            country (str): The name of the country.
            mental_health (int): The mental health score.

        Returns:
            list[dict[Any, Any]]: List of dictionaries representing students in the specified country with the given mental health score.
        """
        with self.database_manager.engine.begin() as connection:
            query = self.__get_base_student_query().where(
                and_(
                    Country.country_name == country,
                    Student.mental_health_score == mental_health,
                )
            )
            self.logger.debug(
                f"Executing query for country: {country} and mental health score: {mental_health}"
            )
            results = connection.execute(query).mappings().all()
        return [dict(result) for result in results]

    def __get_base_student_query(self) -> Select[Any]:
        """
        Get the base student query with joins to related tables.

        Returns:
            Select[Any]: A SQLAlchemy select statement for fetching student data.
        """
        return (
            select(
                Student.id,
                Student.relationship_status,
                Student.age,
                Student.affects_academic_performance,
                Student.sleep_hours_per_night,
                Student.mental_health_score,
                Student.conflicts_over_social_media,
                Student.addicted_score,
                Gender.gender,
                AcademicLevel.academic_level,
                Country.country_name,
            )
            .join(Gender, Student.gender_id == Gender.id)
            .join(AcademicLevel, Student.academic_level_id == AcademicLevel.id)
            .join(Country, Student.country_id == Country.id)
            .join(Platform, Student.platform_id == Platform.id)
        )
