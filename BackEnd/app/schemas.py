from pydantic import BaseModel
from datetime import datetime

class center(BaseModel):
    lat: float
    lon: float

class ShopLocation(BaseModel):
    lat: float
    lon: float
    
class Shop(BaseModel):
    id: int
    name: str
    address: str
    location: ShopLocation
    
    class Config:
        orm_mode = True

class ShopList(BaseModel):
    shop: list[Shop]
    center: center

class ApiKeyOut(BaseModel):
    id: str                     # Unique identifier for the API key response
    apiKey: str                 # The actual API key value
    created_at: datetime        # Timestamp indicating when the API key was provided

    class Config:
        orm_mode = True