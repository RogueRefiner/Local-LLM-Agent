from pydantic import BaseModel


class GenderAndAcademicLevelRequest(BaseModel):
    gender: str
    academic_level: str


class CountryRequest(BaseModel):
    country: str


class ThresholdRequest(BaseModel):
    threshold: int


class AffectedStatusRequest(BaseModel):
    is_affected: bool


class CountryAndMentalHealthRequest(BaseModel):
    country: str
    mental_health_score: int
