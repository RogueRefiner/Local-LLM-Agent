import simplejson as json
from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from data.example.controller.database_controller import (
    DatabaseController,
    get_database_controller,
)
from data.example.utils.EAcademicLevel import EAcademicLevel
from data.example.utils.EGender import EGender
from utils.logger.app_logger import ApplicationLogger, get_application_logger
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

insert_data_env: str = os.getenv("INSERT_EXAMPLE_DATA", "True")
if insert_data_env == "True":
    insert_data = True
else:
    insert_data = False


@router.get("/")
async def health_check():
    """
    Check if the application is healthy.

    Returns:
        dict: A dictionary with a message key indicating health status.
    """
    return JSONResponse(
        content={
            "status": "success",
            "message": "Hello World",
        }
    )


@router.get("/students/import")
async def import_students(
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Import students data from a CSV file into the database.

    Args:
        None

    Returns:
        JSONRepsone: A dictionary with a status key indicating the import completion.
    """
    try:
        api_logger.debug(f"Starting inserting data process - Reading csv file")
        df = db_controller.read_csv(
            Path("example/datasets/Students_Social_Media_Addiction.csv"),
            "Student_ID",
        )

        api_logger.debug(f"Starting inserting data")
        db_controller.insert_data(df)

        api_logger.debug(f"Finished inserting data")
        return JSONResponse(
            content={
                "status": "success",
                "message": "import completed",
            }
        )
    except Exception as e:
        api_logger.error(f"Failed inserting data: {e}")
        return JSONResponse(
            content={
                "status": "failure",
                "message": "import failed",
            }
        )


@router.post("/students/fetch_by_gender_and_level")
async def fetch_by_gender_and_academic_level(
    request: Request,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    # TODO:
    try:
        data = await request.json()
        gender = data.get("gender")
        academic_level = data.get("academic_level")
        api_logger.debug(
            f"Fetching students: gender={gender}, academic_level={academic_level}"
        )
        results = db_controller.fetch_by_gender_and_academic_level(
            gender, academic_level
        )

        return JSONResponse(
            content={
                "status": "success",
                "data": results,
                "count": len(results),
            }
        )
    except Exception as e:
        api_logger.error(f"Failed to fetch students: {e}")
        return JSONResponse(
            content={
                "status": "failure",
                "message": str(e),
            },
            status_code=400,
        )


@router.post("/students/fetch_daily_use_for_country")
async def fetch_daily_use_for_country(
    request: Request,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    # TODO:
    try:
        data = await request.json()
        country = data.get("country")

        api_logger.debug(f"Fetching average daily usage for country: {country}")
        result = db_controller.fetch_avg_daily_usage_for_country(country)
        return JSONResponse(
            content={
                "status": "success",
                "value": json.dumps(result, use_decimal=True),
            }
        )
    except Exception as e:
        api_logger.error(f"Failed to fetch average daily use: {e}")
        return JSONResponse(
            content={"status": "failure", "message": str(e)}, status_code=400
        )


@router.post("/students/fetch_conflicts_over_threshold")
async def fetch_conflicts_over_threshold(
    request: Request,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    # TODO
    try:
        data = await request.json()
        threshold = data.get("threshold")

        api_logger.debug(f"Fetching students with conflict score above: {threshold}")
        results = db_controller.fetch_conflicts_over_threshold(threshold)
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        api_logger.error(f"Failed to fetch students with conflict score: {e}")
        return JSONResponse(
            content={"status": "failure", "message": str(e)}, status_code=400
        )


@router.post("students/fetch_students_by_affected_flag")
async def fetch_students_by_affected_flag(
    request: Request,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    # TODO:
    try:
        data = await request.json()
        is_affected = data.get("is_affected")

        api_logger.debug(f"Fetching students with affected flag: {is_affected}")
        results = db_controller.fetch_students_by_affected_flag(is_affected)
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        api_logger.error(f"Failed to fetch students with affected flag: {e}")
        return JSONResponse(
            content={"status": "failure", "message": str(e)}, status_code=400
        )


@router.post("students/fetch_student_by_country_and_mental_health_threshold")
async def fetch_students_by_country_and_mental_health(
    request: Request,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    # TODO:
    try:
        data = await request.json()
        country = data.get("country")
        mental_health_score = data.get("mental_health_score")

        api_logger.debug(
            f"Fetching students with mental health score: {mental_health_score} in country: {country}"
        )
        results = db_controller.fetch_students_by_country_and_mental_health(
            country, mental_health_score
        )
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        api_logger.error(
            f"Failed to fetch students with mental health threshold from a specific country"
        )
        return JSONResponse(
            content={"status": "failure", "message": str(e)}, status_code=400
        )
