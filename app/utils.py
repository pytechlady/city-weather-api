from fastapi import HTTPException
import httpx
from datetime import datetime


# Function to get the longitude and latitude of a city
def get_city_coordinates(city: str, api_key: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = httpx.get(url)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return data.get('lat'), data.get('lon')
    else:
        raise HTTPException(status_code=404, detail="City not found")
    
    
# Convert date string to date object
def convert_date_string(date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        return date_obj
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

# Funtion to define error message 
def convert_to_error_message(message: any) -> dict:
    return {
        "status": "failure",
        "message": message,
        "data": "null",
    }
    
# Funtion to define success message 
def convert_to_success_message_with_data(data: dict) -> dict:
    return {
        "status": "success",
        "data": data,
    }