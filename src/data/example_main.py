from data.example.controller.database_controller import (
    DatabaseController,
    get_database_controller,
)
from fastapi import FastAPI, Depends
from pathlib import Path
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

insert_data_env: str = os.getenv("INSERT_EXAMPLE_DATA", "True")
if insert_data_env == "True":
    insert_data = True
else:
    insert_data = False


@app.get("/")
async def health_check():
    """
    Check if the application is healthy.

    Returns:
        dict: A dictionary with a message key indicating health status.
    """
    return {"message": "Hello World"}


@app.post("/students/import")
async def import_students(
    db_controller: DatabaseController = Depends(get_database_controller),
):
    """
    Import students data from a CSV file into the   WARNING   WatchFiles detected changes in 'src/data/example_main.py'. Reloading...
    database.

    Args:
        None

    Returns:
        dict: A dictionary with a status key indicating the import completion.
    """
    df = db_controller.read_csv(
        Path("src/data/example/datasets/Students_Social_Media_Addiction.csv"),
        "Student_ID",
    )
    db_controller.insert_data(df)
    return {"status": "import completed"}
