from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, Double, ForeignKey, Integer, Text
from sqlalchemy import Enum as SQLEnum
from ..utils.EGender import EGender
from ..utils.EAcademicLevel import EAcademicLevel
from ..utils.EPlatform import EPlatform
from ..utils.ERelationshipStatus import ERelationshipStatus


class Base(DeclarativeBase):
    pass


class Student(Base):
    """
    The primary fact table representing individual student survey responses.
    This table links demographic data with social media usage patterns and
    psychological health metrics.
    mental_health_score: 1 (Poor) to 10 (Excellent)
    addicted_score: 1 (not addicted at all) to 5 (highly addicted)
    """

    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id"))
    academic_level_id: Mapped[int] = mapped_column(ForeignKey("academic_levels.id"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"))

    relationship_status: Mapped[ERelationshipStatus] = mapped_column(
        SQLEnum(
            ERelationshipStatus,
            name="erelationshipstatus",
            native_enum=True,
            validate_strings=False,
        ),
        nullable=False,
    )
    age: Mapped[int] = mapped_column(Integer)

    avg_daily_usage_hours: Mapped[int] = mapped_column(Integer)
    affects_academic_performance: Mapped[bool] = mapped_column(Boolean)
    sleep_hours_per_night: Mapped[float] = mapped_column(Double)

    mental_health_score: Mapped[int] = mapped_column(Integer)
    conflicts_over_social_media: Mapped[int] = mapped_column(Integer)
    addicted_score: Mapped[int] = mapped_column(Integer)


class Gender(Base):
    """
    Lookup table for gender identities.
    Maps to the EGender enum (male, female).
    """

    __tablename__ = "genders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[EGender] = mapped_column(
        SQLEnum(
            EGender,
            name="egender",
            native_enum=True,
            validate_strings=False,
        ),
        nullable=False,
    )


class AcademicLevel(Base):
    """
    Lookup table for the student's current stage of education.
    Maps to the EAcademicLevel enum (undergraduate, graduate, high school)
    """

    __tablename__ = "academic_levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    academic_level: Mapped[EAcademicLevel] = mapped_column(
        SQLEnum(
            EAcademicLevel,
            name="eacademiclevel",
            native_enum=True,
            validate_strings=False,
        ),
        nullable=False,
    )


class Country(Base):
    """
    Geographical dimension table.
    Stores the name of the country where the student resides.
    """

    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_name: Mapped[str] = mapped_column(Text)


class Platform(Base):
    """
    Lookup table for social media platforms.
    Maps to the EPlatform enum (instagram, twitter, tik tok, youtube, facebook,
      linkedin, snapchat, line, kakaotalk, vkontakte, whatsapp, wechat)
    """

    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[EPlatform] = mapped_column(
        SQLEnum(
            EPlatform,
            name="eplatform",
            native_enum=True,
            validate_strings=False,
        ),
        nullable=False,
    )
