from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DATETIME
from .db_setup import Base
    
class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class ShopLocation(Base):
    __tablename__ = "shopLocation"

    id = Column(Integer, primary_key=True, nullable=False)
    shopId = Column(Integer, ForeignKey('shop.id'), nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)

class ApiKey(Base):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True, nullable=False)
    apiKey_id = Column(String(255), unique=True, nullable=False)
    apiKey = Column(LONGTEXT, nullable=False)
    created_at = Column(DATETIME(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
