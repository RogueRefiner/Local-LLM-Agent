from pydantic import BaseModel


class GenderAndAcademicLevelRequest(BaseModel):
    """
    Fetch students by gender and academic level.

    Args:
        gender (EGender): The gender of the student.
        academic_level (EAcademicLevel): The academic level of the student.

    Returns:
        list[dict[Any, Any]]: A list of dictionaries containing student data.
    """

    gender: str
    academic_level: str


class CountryRequest(BaseModel):
    """
    Fetch average daily usage for a specific country.

    Args:
        country (str): The name of the country.

    Returns:
        Decimal | None: The average daily usage hours or None if no results found.
    """

    country: str


class ThresholdRequest(BaseModel):
    """
    Fetch students with conflicts over threshold.

    Args:
        threshold (int): The threshold value.

    Returns:
        list[dict[Any, Any]]: A list of dictionaries containing student data.
    """

    threshold: int


class AffectedStatusRequest(BaseModel):
    """
    Fetch students by affected flag.

    Args:
        is_affected (bool): Whether the student is affected.

    Returns:
        list[dict[Any, Any]]: A list of dictionaries containing student data.
    """

    is_affected: bool


class CountryAndMentalHealthRequest(BaseModel):
    """
    Fetch students by country and mental health score.

    Args:
        country (str): The name of the country.
        mental_health (int): The mental health score of the student.

    Returns:
        list[dict[Any, Any]]: A list of dictionaries containing student data.
    """

    country: str
    mental_health_score: int
