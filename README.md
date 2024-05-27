# Task Scheduling Backend


This repository contains the backend server for the Task Scheduling front-end. The backend is responsible for processing the logical model, running scheduling algorithms, and communicating with the frontend. It is built with FastAPI and provides a RESTful API for interaction with the [frontend](https://eslab2.pages.dev/).

## Table of Contents
- [Technologies Used](#technologies-used)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Input and Output Schemas](#input-and-output-formats)
- [Running the Server](#running-the-server)
- [Components](#components)
- [Contributing](#contributing)

## Technologies Used

- [Python 3](https://www.python.org/about/gettingstarted/)
- [FastAPI](https://fastapi.tiangolo.com/learn/)
- [NetworkX](https://networkx.org/documentation/stable/tutorial.html)
- [Uvicorn](https://www.uvicorn.org/)

## Features
- **[RESTful](https://en.wikipedia.org/wiki/REST) API**: Provides endpoints for scheduling tasks and retrieving schedules.
- **Multiple Scheduling Algorithms**: Implements LDF and EDF scheduling algorithms for task scheduling.
- **Input Validation**: Ensures valid data format for processing.
- **[Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) (CORS)**: Enabled for specified origins.

## API Endpoints

- **POST /schedule_jobs**: Accepts a task graph in JSON format and returns the scheduled tasks using four different algorithms.
- **GET /get_jobs**: Endpoint for retrieving job schedules.
- **GET /**: Root endpoint to verify if the server is running.

Learn more about [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

## Input and Output Schemas

### API Input Schema for /schedule_jobs

The backend expects input in the following [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) schema:

    ```json
    {
    "application": {
        "jobs": [
        {
            "id": <integer>,
            "wcet_fullspeed": <integer>,
            "mcet": <integer>,
            "deadline": <integer>
        },
        ...
        ],
        "messages": [
        {
            "id": <integer>,
            "sender": <integer>,
            "receiver": <integer>,
            "size": <integer>,
            "timetriggered": <boolean>
        },
        ...
        ]
    },
    "platform": {
        "nodes": [
        {
            "id": <integer>,
            "is_router": <boolean>
        },
        ...
        ],
        "links": [
        {
            "start": <integer>,
            "end": <integer>
        },
        ...
        ]
    }
    }
    ```

### Output Schema for /schedule_jobs

    The backend returns output in the following JSON format:

    ```json
    {
    "schedule1": [
        {
        "job_id": <integer>,
        "node_id": <integer>,
        "end_time": <integer>,
        "deadline": <integer>,
        "start_time": <integer>,
        "execution_time": <integer>
        },
        ...
    ],
    "schedule2": [
        {
        "job_id": <integer>,
        "node_id": <integer>,
        "end_time": <integer>,
        "deadline": <integer>,
        "start_time": <integer>,
        "execution_time": <integer>
        },
        ...
    ],
    "schedule3": [
        {
        "job_id": <integer>,
        "node_id": <integer>,
        "end_time": <integer>,
        "deadline": <integer>,
        "start_time": <integer>,
        "execution_time": <integer>
        },
        ...
    ],
    "schedule4": [
        {
        "job_id": <integer>,
        "node_id": <integer>,
        "end_time": <integer>,
        "deadline": <integer>,
        "start_time": <integer>,
        "execution_time": <integer>
        },
        ...
    ]
    }
    ```
## Running the Server

1. Clone the repository:
    git clone https://github.com/linem-davton/graphdraw-eslab-backend.git

2. Navigate to the project directory:
    cd graphdraw-eslab-backend

3. Install dependencies:
    pip install -r requirements.txt

5. Start the development server:
   python3 src/backend.py

6. Access the API:
   The backend server will be running at http://localhost:8000.
  If everything is set up correctly, you should see the following message: {"Hello": "World"}

## Components

- **backend.py**: Main entry point for the FastAPI backend server.
    - Handles API endpoints and routing.
    - Configures CORS middleware.
- **algorithms.py**: Contains the implementation of the scheduling algorithms (LDF, EDF).
    - ldf_algorithm: Implementation of the LDF scheduling algorithm.
    - edf_schedule: Implementation of the EDF scheduling algorithm.
    - ldf_singlecore: Implementation of the single-core LDF scheduling algorithm.
    - edf_singlecore: Implementation of the single-core EDF scheduling algorithm.
- **config.json**: Configuration file for backend settings.
- **requirements.txt**: File listing all the dependencies required for the project.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature-name).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/your-feature-name).
- Create a new Pull Request.

## Resources and References
