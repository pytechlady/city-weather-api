import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from .database import get_db
from datetime import datetime
from app import models
from app import utils
from app.database import engine

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Create all table in the database
models.Base.metadata.create_all(bind=engine)

API_KEY = os.getenv('API_KEY')

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def get_city_weather(city: str, date: str, db: db_dependency):
    
    date_obj = utils.convert_date_string(date)
    
    # Check if the requested city and date already exist in the database
    city_weather = db.query(models.CityData).filter(models.CityData.city==city, models.CityData.date==date_obj).first()
    
    if city_weather:
        response_data = {
                "City name is": city_weather.city,
                "The date is": city_weather.date,
                "Minimum temperature": city_weather.min_temp,
                "Maximum temperature": city_weather.max_temp,
                "Average temperature": city_weather.avg_temp,
                "Humidity": city_weather.humidity
        }
        return utils.convert_to_success_message_with_data(response_data)
    
    # If no match in the database make an API request to get the weather data    
    else:
        lat, lon = utils.get_city_coordinates(city, API_KEY)
        url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={API_KEY}"
        
        response = httpx.get(url)
        if response.status_code == 200:
            data = response.json()
            
            city_weather = models.CityData(
                city=city,
                date=date_obj,
                min_temp = data['temperature']['min'],
                max_temp = data['temperature']['max'],
                avg_temp = round(sum([int(data['temperature']['min']), int(data['temperature']['max'])]) / 2, 2),
                humidity = data['humidity']['afternoon']
            )
            
            # Save the weather data to the database for subsequent requests.
            db.add(city_weather)
            
            db.commit()
            db.refresh(city_weather)
            
            response_data = {
                "City name is": city,
                "The date is": date,
                "Minimum temperature": city_weather.min_temp,
                "Maximum temperature": city_weather.max_temp,
                "Average temperature": city_weather.avg_temp,
                "Humidity": city_weather.humidity,
            }
            return utils.convert_to_success_message_with_data(response_data)
            
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from OpenWeather API.")