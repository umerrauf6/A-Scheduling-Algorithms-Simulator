"""
This module defines the FastAPI app and its routes for scheduling jobs. When run as a script, it starts a uvicorn server on port defined in the config.py file.

The app uses CORS middleware to handle cross-origin requests and defines endpoints to schedule jobs and retrieve job information. It interacts with the `algorithms` module
to calculate schedules based on different scheduling algorithms.

Endpoints:
- POST /schedule_jobs: Accepts JSON payload to schedule jobs based on application and platform data.
- GET /: Provides a basic test endpoint to confirm the app is running.

See the function docstrings within this module for more detailed API documentation.
"""

__author__ = "Utkarsh Raj"
__version__ = "1.0.0"

from http.client import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from config import SERVER_PORT, SERVER_HOST

import algorithms as alg

app = FastAPI()
origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://eslab2.pages.dev",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/schedule_jobs")
def schedule_jobs(data: dict):
    """
    Schedule jobs based on the provided application and platform data.

    This endpoint processes a JSON payload containing application and platform configurations,
    then calculates schedules using Least Deadline First (LDF), Earliest Deadline First (EDF),
    Rate Monotonic (RMS) and Least Laxity (LL) scheduling algorithms
    on single-core setups.

    Args:
        data (dict): A dictionary containing 'application' and 'platform' data necessary for scheduling.

    Raises:
        HTTPException: If the 'application' or 'platform' data is missing or malformed, a 400 error is raised.

    Returns:
        dict: A dictionary containing schedules calculated using different algorithms:
              - schedule1: Schedule using Latest Deadline First (LDF) schedulin on single-core.
              - schedule2: Schedule using Earliest Deadline First (EDF) scheduling on single-core.
              - schedule3: Schedule using Rate Monotonic Scheduling (RMS) on single-core.
              - schedule4: Schedule using Least Laxity (LL) on single-core.
    """

    print("Received JSON data:", json.dumps(data, indent=4))
    application_data = data.get("application")
    platform_data = data.get("platform")

    if not application_data or not platform_data:
        raise HTTPException(status_code=400, detail="Invalid data format")

    ldf_schedule = alg.ldf_singlecore(application_data)
    edf_schedule = alg.edf_singlecore(application_data)
    rms_schedule = alg.rms_singlecore(application_data)
    ll_schedule = alg.ll_singlecore(application_data)

    response = {
        "schedule1": ldf_schedule,
        "schedule2": edf_schedule,
        "schedule3": rms_schedule,
        "schedule4": ll_schedule,
    }

    print(json.dumps(response, indent=4))
    return response


@app.get("/")
def read_root():
    """
    Retrieve the root URL. For testing purposes.

    Returns:
        dict: A simple dictionary with a greeting.
    """
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")
