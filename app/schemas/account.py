from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class AccountCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "account_holder_name": "Juan Perez",
                "balance": 1000.50
            }
        }
    )
    
    account_holder_name: str = Field(
        ..., 
        description="Nombre del titular de la cuenta (mínimo 3 caracteres)"
    )
    balance: float = Field(
        default=0.0, 
        description="Saldo inicial de la cuenta (debe ser mayor o igual a 0)"
    )
    
    @field_validator('account_holder_name')
    @classmethod
    def validate_account_holder_name(cls, v):
        if len(v) < 3:
            raise ValueError('El nombre del titular debe tener al menos 3 caracteres')
        if len(v) > 100:
            raise ValueError('El nombre del titular no puede tener más de 100 caracteres')
        return v
    
    @field_validator('balance')
    @classmethod
    def validate_balance(cls, v):
        if v < 0:
            raise ValueError('El saldo no puede ser negativo')
        return v

class AccountUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "account_holder_name": "Carlos García",
                "amount": 500.00
            }
        }
    )
    
    account_holder_name: Optional[str] = Field(
        None, 
        description="Nuevo nombre del titular de la cuenta (opcional)"
    )
    amount: Optional[float] = Field(
        None, 
        description="Cantidad a agregar o restar del saldo (opcional)"
    )
    
    @field_validator('account_holder_name')
    @classmethod
    def validate_account_holder_name(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError('El nombre del titular debe tener al menos 3 caracteres')
            if len(v) > 100:
                raise ValueError('El nombre del titular no puede tener más de 100 caracteres')
        return v
    
    def model_post_init(self, __context):
        """Valida que al menos un campo sea proporcionado después de la inicialización."""
        if self.account_holder_name is None and self.amount is None:
            raise ValueError('Debe proporcionar al menos el nombre del titular o una cantidad para actualizar')

class AccountResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra = {
            "example": {
                "id": "60a7e0e7a1b2c3d4e5f6a7b8",
                "account_holder_name": "Juan Perez",
                "balance": 1500.50
            }
        }
    )
    
    id: str
    account_holder_name: str
    balance: float
