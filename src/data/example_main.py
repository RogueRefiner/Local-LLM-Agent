from data.example.controller.database_controller import DatabaseController
from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv
import os

db_controller: DatabaseController = DatabaseController()
app = FastAPI()
load_dotenv()

insert_data_env: str = os.getenv("INSERT_EXAMPLE_DATA", "True")
if insert_data_env == "True":
    insert_data = True
else:
    insert_data = False


@app.get("/")
async def root():
    if insert_data:
        df = db_controller.read_csv(
            Path("src/data/example/datasets/Students_Social_Media_Addiction.csv"),
            "Student_ID",
        )
        db_controller.insert_data(df)
    return {"message": "Hello World"}
