from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

from dotenv import load_dotenv

load_dotenv()


client = TestClient(app)

def test_get_existing_city_weather_data_from_db():
    resp = client.get('/', params={'city': 'Ibiza', 'date': '2024-08-19'})
    assert resp.status_code == 200

    response_data = resp.json()

    assert "status" in response_data
    assert "data" in response_data
    assert response_data["status"] == "success"

    assert "City name is" in response_data["data"]
    assert "The date is" in response_data["data"]
    assert "Minimum temperature" in response_data["data"]
    assert "Maximum temperature" in response_data["data"]
    assert "Average temperature" in response_data["data"]
    assert "Humidity" in response_data["data"]
    
def test_city_not_found():
    resp = client.get('/', params={'city': '-', 'date': '2024-09-01'})
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'City not found'}
    
def test_invalid_date_format():
    resp = client.get('/', params={'city': 'London', 'date': '01-9-2021'})
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'Invalid date format. Please use YYYY-MM-DD.'}
    
def test_fetch_city_weather_data_from_external_api():
    city = "Paris"
    date = "2024-10-10"

    # Mock data to be returned by the external API
    mock_api_data = {
        'lat': 48.8566,
        'lon': 2.3522,
        'tz': '+02:00',
        'date': date,
        'units': 'standard',
        'cloud_cover': {'afternoon': 35.0},
        'humidity': {'afternoon': '70'},
        'precipitation': {'total': 0.0},
        'temperature': {
            'min': '283.15',
            'max': '290.15',
            'afternoon': 287.15,
            'night': 284.15,
            'evening': 288.15,
            'morning': 285.15
        },
        'pressure': {'afternoon': 1015.0},
        'wind': {'max': {'speed': 5.0, 'direction': 270}}
    }

    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_data

        response = client.get("/", params={"city": city, "date": date})
        assert response.status_code == 200

        response_data = response.json()["data"]

        # Verify the returned weather data
        assert response_data["City name is"] == city
        assert response_data["The date is"] == date
        assert response_data["Minimum temperature"] == mock_api_data["temperature"]['min']
        assert response_data["Maximum temperature"] == mock_api_data["temperature"]['max']
        assert response_data["Humidity"] == mock_api_data['humidity']['afternoon']