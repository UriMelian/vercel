from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria: Optional[str] = None


class ProductCreate(ProductBase):
    pass
class Product(ProductBase):    
    id: UUID