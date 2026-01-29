from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from data.example.controller.database_controller import (
    DatabaseController,
    get_database_controller,
)
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
        dict: A dictionary with a message key indicating health status. #TODO:
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
):
    """
    Import students data from a CSV file into the database.

    Args:
        None

    Returns:
        dict: A dictionary with a status key indicating the import completion. #TODO:
    """

    api_logger.debug(f"Starting inserting data process - Reading csv file")
    df = db_controller.read_csv(
        Path("example/datasets/Students_Social_Media_Addiction.csv"),
        "Student_ID",
    )
    api_logger.debug(f"Starting inserting data")
    # TODO: try except
    db_controller.insert_data(df)
    api_logger.debug(f"Finished inserting data")
    return JSONResponse(
        content={
            "status": "success",
            "message": "import completed",
        }
    )
