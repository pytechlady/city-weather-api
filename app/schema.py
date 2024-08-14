from pydantic import BaseModel
from datetime import date

# Create database tables with the following fields
class WeatherData(BaseModel):
    id: int
    city: str
    date: date
    min_temp: str
    max_temp: str
    avg_temp: str
    humidity: str
    
    # To ensure that Pydantic can read data from SQLAlchemy models directly
    class Config:
        orm_mode = True