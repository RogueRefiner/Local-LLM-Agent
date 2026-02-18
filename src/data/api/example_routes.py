import simplejson as json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from utils.request_models import (
    GenderAndAcademicLevelRequest,
    AffectedStatusRequest,
    CountryAndMentalHealthRequest,
    CountryRequest,
    ThresholdRequest,
)
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


@router.get(
    "/students/import",
    responses={
        200: {
            "description": "Successful insertion of the csv file",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message": "import completed"}
                }
            },
        },
        400: {
            "description": "Insertion of the csv file failed",
        },
    },
)
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
            },
            status_code=200,
        )
    except Exception as e:
        api_logger.error(f"Failed inserting data: {e}")
        raise HTTPException(status_code=400, detail="import failed")


@router.post(
    "/students/fetch_by_gender_and_level",
    responses={
        200: {
            "description": "Fetch all students with a specific gender and academic level",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": "[{'id':703,'relationship_status':'IN RELATIONSHIP','age':21,'affects_academic_performance':true,'sleep_hours_per_night':6.7,'mental_health_score':6,'conflicts_over_social_media':3,'addicted_score':7,'gender':'FEMALE','academic_level':'UNDERGRADUATE','country_name':'China'},"
                        "{'id':705,'relationship_status':'SINGLE','age':19,'affects_academic_performance':true,'sleep_hours_per_night':6.3,'mental_health_score':5,'conflicts_over_social_media':4,'addicted_score':8,'gender': 'FEMALE','academic_level':'UNDERGRADUATE','country_: '100'  name':'Poland'}]",
                        "count": "2",
                    }
                }
            },
        },
        400: {
            "description": "Failed to fetch students based on a gender and the academic level"
        },
    },
)
async def fetch_by_gender_and_academic_level(
    request: GenderAndAcademicLevelRequest,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Fetches students based on gender and academic level.

    Args:
        request (GenderAndAcademicLevelRequest): The request containing gender and academic level filters.
        db_controller (DatabaseController, optional): Dependency injection for database controller. Defaults to Depends(get_database_controller).
        api_logger (ApplicationLogger, optional): Dependency injection for API logger. Defaults to Depends(get_application_logger).

    Returns:
        JSONResponse: A response containing the status of the operation, fetched data, and count.
    """
    try:
        api_logger.debug(
            f"Fetching students: gender={request.gender}, academic_level={request.academic_level}"
        )
        results = db_controller.fetch_by_gender_and_academic_level(
            EGender(request.gender), EAcademicLevel(request.academic_level)
        )

        return JSONResponse(
            content={
                "status": "success",
                "data": results,
                "count": len(results),
            },
            status_code=200,
        )
    except Exception as e:
        error = f"Failed to fetch students: {e}"
        api_logger.error(error)
        raise HTTPException(status_code=400, detail=error)


@router.post(
    "/students/fetch_daily_use_for_country",
    responses={
        200: {
            "description": "Fetch average daily usage for all students from a country",
            "context": {
                "application/json": {"example": {"status": "success", "value": "5.26"}}
            },
        },
        400: {"description": "Failed to fetch average daily use for a country"},
    },
)
async def fetch_daily_use_for_country(
    request: CountryRequest,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Fetches average daily usage for a given country.

    Args:

        request (CountryRequest): The request containing the target country.
        db_controller (DatabaseController, optional): Dependency injection for database controller. Defaults to Depends(get_database_controller).
        api_logger (ApplicationLogger, optional): Dependency injection for API logger. Defaults to Depends(get_application_logger).

    Returns:
        JSONResponse: A response containing the status of the operation and the average daily usage data.
    """
    try:
        api_logger.debug(f"Fetching average daily usage for country: {request.country}")
        result = db_controller.fetch_avg_daily_usage_for_country(request.country)
        return JSONResponse(
            content={
                "status": "success",
                "value": json.dumps(result, use_decimal=True),
            }
        )
    except Exception as e:
        error = f"Failed to fetch average daily use: {e}"
        api_logger.error(error)
        raise HTTPException(status_code=400, detail=error)


@router.post(
    "/students/fetch_conflicts_over_threshold",
    responses={
        200: {
            "description": "Fetch all students with a certain conflict score",
            "context": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": "[{'id':703,'relationship_status':'IN RELATIONSHIP','age':21,'affects_academic_performance':true,'sleep_hours_per_night':6.7,'mental_health_score':6,'conflicts_over_social_media':3,'addicted_score':7,'gender':'FEMALE','academic_level':'UNDERGRADUATE','country_name':'China'},"
                        "{'id':705,'relationship_status':'SINGLE','age':19,'affects_academic_performance':true,'sleep_hours_per_night':6.3,'mental_health_score':5,'conflicts_over_social_media':3,'addicted_score':8,'gender': 'FEMALE','academic_level':'UNDERGRADUATE','country_: '100'  name':'Poland'}]",
                        "count": "2",
                    }
                }
            },
        },
        400: {"description": "Faield to fetch students with conflict score"},
    },
)
async def fetch_conflicts_over_threshold(
    request: ThresholdRequest,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Fetches students with conflict scores above a given threshold.

    Args:
        request (ThresholdRequest): The request containing the conflict score threshold.
        db_controller (DatabaseController, optional): Dependency injection for database controller. Defaults to Depends(get_database_controller).
        api_logger (ApplicationLogger, optional): Dependency injection for API logger. Defaults to Depends(get_application_logger).

    Returns:
        JSONResponse: A response containing the status of the operation, fetched data, and count.
    """
    try:
        api_logger.debug(
            f"Fetching students with conflict score above: {request.threshold}"
        )
        results = db_controller.fetch_conflicts_over_threshold(request.threshold)
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        error = f"Failed to fetch students with conflict score: {e}"
        api_logger.error(error)
        raise HTTPException(status_code=400, detail=error)


@router.post(
    "students/fetch_students_by_affected_flag",
    responses={
        200: {
            "description": "Fecth all students with the specific affected flag",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "value": "[{'id':703,'relationship_status':'IN RELATIONSHIP','age':21,'affects_academic_performance':true,'sleep_hours_per_night':6.7,'mental_health_score':6,'conflicts_over_social_media':3,'addicted_score':7,'gender':'FEMALE','academic_level':'UNDERGRADUATE','country_name':'China'},"
                        "{'id':705,'relationship_status':'SINGLE','age':19,'affects_academic_performance':true,'sleep_hours_per_night':6.3,'mental_health_score':5,'conflicts_over_social_media':4,'addicted_score':8,'gender': 'FEMALE','academic_level':'UNDERGRADUATE','country_: '100'  name':'Poland'}]",
                        "count": "2",
                    }
                }
            },
        },
        400: {
            "description": "Failed to fetch students with the affected flag either being true or false, depending on the query parameter"
        },
    },
)
async def fetch_students_by_affected_flag(
    request: AffectedStatusRequest,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Fetches students based on their affected flag.

    Args:
        request (AffectedStatusRequest): The request containing the affected flag status.
        db_controller (DatabaseController, optional): Dependency injection for database controller. Defaults to Depends(get_database_controller).
        api_logger (ApplicationLogger, optional): Dependency injection for API logger. Defaults to Depends(get_application_logger).

    Returns:
        JSONResponse: A response containing the status of the operation, fetched data, and count.
    """
    try:
        api_logger.debug(f"Fetching students with affected flag: {request.is_affected}")
        results = db_controller.fetch_students_by_affected_flag(request.is_affected)
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        error = f"Failed to fetch students with affected flag: {e}"
        api_logger.error(error)
        raise HTTPException(status_code=400, detail=error)


@router.post(
    "students/fetch_student_by_country_and_mental_health_threshold",
    responses={
        200: {
            "description": "Fetched all students from a specific country with a specific mental health score",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "value": "[{'id':703,'relationship_status':'IN RELATIONSHIP','age':21,'affects_academic_performance':true,'sleep_hours_per_night':6.7,'mental_health_score':6,'conflicts_over_social_media':3,'addicted_score':7,'gender':'FEMALE','academic_level':'UNDERGRADUATE','country_name':'China'},"
                        "{'id':705,'relationship_status':'SINGLE','age':19,'affects_academic_performance':true,'sleep_hours_per_night':6.3,'mental_health_score':6,'conflicts_over_social_media':4,'addicted_score':8,'gender': 'FEMALE','academic_level':'UNDERGRADUATE','country_: '100'  name':'China'}]",
                        "count": "2",
                    }
                }
            },
        },
        400: {
            "description": "Failed to fetch all students from a country with the specific mental health score"
        },
    },
)
async def fetch_students_by_country_and_mental_health(
    request: CountryAndMentalHealthRequest,
    db_controller: DatabaseController = Depends(get_database_controller),
    api_logger: ApplicationLogger = Depends(get_application_logger),
) -> JSONResponse:
    """
    Fetches students based on their mental health score within a specific country.

    Args:
        request (CountryAndMentalHealthRequest): The request containing the target country and mental health score threshold.
        db_controller (DatabaseController, optional): Dependency injection for database controller. Defaults to Depends(get_database_controller).
        api_logger (ApplicationLogger, optional): Dependency injection for API logger. Defaults to Depends(get_application_logger).

    Returns:
        JSONResponse: A response containing the status of the operation, fetched data, and count.
    """
    try:
        api_logger.debug(
            f"Fetching students with mental health score: {request.mental_health_score} in country: {request.country}"
        )
        results = db_controller.fetch_students_by_country_and_mental_health(
            request.country, request.mental_health_score
        )
        return JSONResponse(
            content={"status": "success", "value": results, "count": len(results)}
        )
    except Exception as e:
        error = f"Failed to fetch students with mental health threshold from a specific country: {e}"
        api_logger.error(error)
        raise HTTPException(status_code=400, detail=error)
