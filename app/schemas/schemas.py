from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    quantity: int = 0
    category: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    location_id: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    sku: str
    name: str
    description: Optional[str]
    quantity: int
    category: Optional[str]
    location_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseLocationCreate(BaseModel):
    percha: int
    piso: int
    columna: int


class WarehouseLocationResponse(BaseModel):
    id: str
    percha: int
    piso: int
    columna: int
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseStructureCreate(BaseModel):
    name: str
    total_perchas: int
    total_pisos: int
    total_columnas: int


class WarehouseStructureUpdate(BaseModel):
    name: Optional[str] = None
    total_perchas: Optional[int] = None
    total_pisos: Optional[int] = None
    total_columnas: Optional[int] = None


class WarehouseStructureResponse(BaseModel):
    id: str
    name: str
    total_perchas: int
    total_pisos: int
    total_columnas: int
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_products: int
    total_locations: int
    occupied_locations: int
    available_locations: int
    low_stock_products: int
