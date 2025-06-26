from pydantic import BaseModel, Field
from typing import Optional

class AccountCreate(BaseModel):
    account_holder_name: str = Field(..., min_length=3, max_length=100)
    balance: float = Field(default=0.0, ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "account_holder_name": "Juan Perez",
                "balance": 1000.50
            }
        }

class AccountUpdate(BaseModel):
    amount: float = Field(..., description="Cantidad a agregar o restar del saldo.")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 500.00
            }
        }

class AccountResponse(BaseModel):
    id: str = Field(..., alias="_id")
    account_holder_name: str
    balance: float

    class Config:
        populate_by_name = True # Permite usar el nombre del campo en lugar del alias al crear la instancia
        json_encoders = {str: lambda x: str(x) if isinstance(x, str) else x} # Para _id
        json_schema_extra = {
            "example": {
                "id": "60a7e0e7a1b2c3d4e5f6a7b8",
                "account_holder_name": "Juan Perez",
                "balance": 1500.50
            }
        }