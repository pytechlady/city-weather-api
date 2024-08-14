from sqlalchemy import Column, String, Integer, Date
from app.database import Base


class CityData(Base):
    __tablename__ = 'city_weather'
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    date = Column(Date)
    min_temp = Column(String)
    max_temp = Column(String)
    avg_temp = Column(String)
    humidity = Column(String)