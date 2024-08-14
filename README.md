### Project Description:
- RESTful API to serve weather data using data from http://openweathermap.org/api. An API that will get data from a weather API and return the minimum, maximum, average temperature, and humidity for a given city and day.

### Installations

## Prerequisites
- Python 3.9+
- Fastapi
- PostgreSQL
- API_KEY to use openweathermap API

### Setup

## Setup using Docker
 - Change your database connection as desired
 - Run "docker build -t tagname ." (Make sure to include the dot at the end to define the current working directory)
 - Run "docker run --env-file .env -p 8000:8000 -d tagname" (You can remove the '-d' if you don't want to run in detach mode, and also remove the '--env-file . env' if you dont have any environment variables)
 - Run "docker logs -f container_id" to see the logs if you're running in detach mode

## Setup without Docker
- Change your database connection as desired
- 'pip install -r requirements.txt' to install dependencies
- Create a .env file in the root directory and add the necessary environment variables
- Run server 'uvicorn app.main:app --reload'

### Testing
- Run 'pytest app.test.py'

### Usage
- FastAPI automatically generates interactive API documentation at /docs (Swagger UI). So you can check for exaple 'http://localhost:8000/docs' without docker or 'http://0.0.0.0:8000/docs.