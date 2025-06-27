from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum

class DocumentType(str, Enum):
    CC = "CC"  # Cédula de Ciudadanía
    CE = "CE"  # Cédula de Extranjería
    TI = "TI"  # Tarjeta de Identidad
    PP = "PP"  # Pasaporte
    NIT = "NIT"  # Número de Identificación Tributaria

class AccountCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "account_number": "ACC-001",
                "account_type": "savings",
                "customer_name": "Juan Pérez García",
                "document_type": "CC",
                "document_number": "12345678",
                "phone": "+57 300 123 4567",
                "email": "juan.perez@email.com",
                "address": "Calle 123 #45-67, Bogotá",
                "balance": 1000.50
            }
        }
    )
    
    account_number: str = Field(
        ...,
        description="Número de cuenta único"
    )
    account_type: str = Field(
        ...,
        description="Tipo de cuenta (savings, checking, etc.)"
    )
    customer_name: str = Field(
        ..., 
        description="Nombre completo del titular de la cuenta (mínimo 3 caracteres)"
    )
    document_type: DocumentType = Field(
        ...,
        description="Tipo de documento de identificación"
    )
    document_number: str = Field(
        ...,
        description="Número de documento de identificación"
    )
    phone: str = Field(
        ...,
        description="Número de teléfono del titular"
    )
    email: str = Field(
        ...,
        description="Correo electrónico del titular"
    )
    address: str = Field(
        ...,
        description="Dirección de residencia del titular"
    )
    balance: float = Field(
        default=0.0, 
        description="Saldo inicial de la cuenta (debe ser mayor o igual a 0)"
    )
    
    @field_validator('customer_name')
    @classmethod
    def validate_customer_name(cls, v):
        if len(v) < 3:
            raise ValueError('El nombre del titular debe tener al menos 3 caracteres')
        if len(v) > 100:
            raise ValueError('El nombre del titular no puede tener más de 100 caracteres')
        return v
    
    @field_validator('document_number')
    @classmethod
    def validate_document_number(cls, v):
        if len(v) < 3:
            raise ValueError('El número de documento debe tener al menos 3 caracteres')
        if len(v) > 20:
            raise ValueError('El número de documento no puede tener más de 20 caracteres')
        return v.strip()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if len(v) < 7:
            raise ValueError('El teléfono debe tener al menos 7 caracteres')
        if len(v) > 20:
            raise ValueError('El teléfono no puede tener más de 20 caracteres')
        return v.strip()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        if len(v) < 5:
            raise ValueError('El email debe tener al menos 5 caracteres')
        if len(v) > 100:
            raise ValueError('El email no puede tener más de 100 caracteres')
        return v.lower().strip()
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        if len(v) < 10:
            raise ValueError('La dirección debe tener al menos 10 caracteres')
        if len(v) > 200:
            raise ValueError('La dirección no puede tener más de 200 caracteres')
        return v.strip()
    
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
                "account_number": "ACC-002",
                "account_type": "checking",
                "customer_name": "Juan Carlos Pérez García",
                "document_type": "CC",
                "document_number": "87654321",
                "phone": "+57 301 987 6543",
                "email": "juan.carlos@email.com",
                "address": "Carrera 45 #67-89, Medellín",
                "amount": 500.00
            }
        }
    )
    
    account_number: Optional[str] = Field(
        None,
        description="Nuevo número de cuenta (opcional)"
    )
    account_type: Optional[str] = Field(
        None,
        description="Nuevo tipo de cuenta (opcional)"
    )
    customer_name: Optional[str] = Field(
        None, 
        description="Nuevo nombre del titular de la cuenta (opcional)"
    )
    document_type: Optional[DocumentType] = Field(
        None,
        description="Nuevo tipo de documento de identificación (opcional)"
    )
    document_number: Optional[str] = Field(
        None,
        description="Nuevo número de documento de identificación (opcional)"
    )
    phone: Optional[str] = Field(
        None,
        description="Nuevo número de teléfono del titular (opcional)"
    )
    email: Optional[str] = Field(
        None,
        description="Nuevo correo electrónico del titular (opcional)"
    )
    address: Optional[str] = Field(
        None,
        description="Nueva dirección de residencia del titular (opcional)"
    )
    amount: Optional[float] = Field(
        None, 
        description="Cantidad a agregar o restar del saldo (opcional)"
    )
    
    @field_validator('customer_name')
    @classmethod
    def validate_customer_name(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError('El nombre del titular debe tener al menos 3 caracteres')
            if len(v) > 100:
                raise ValueError('El nombre del titular no puede tener más de 100 caracteres')
        return v
    
    @field_validator('document_number')
    @classmethod
    def validate_document_number(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError('El número de documento debe tener al menos 3 caracteres')
            if len(v) > 20:
                raise ValueError('El número de documento no puede tener más de 20 caracteres')
        return v.strip() if v else v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            if len(v) < 7:
                raise ValueError('El teléfono debe tener al menos 7 caracteres')
            if len(v) > 20:
                raise ValueError('El teléfono no puede tener más de 20 caracteres')
        return v.strip() if v else v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            if '@' not in v:
                raise ValueError('El email debe tener un formato válido')
            if len(v) < 5:
                raise ValueError('El email debe tener al menos 5 caracteres')
            if len(v) > 100:
                raise ValueError('El email no puede tener más de 100 caracteres')
        return v.lower().strip() if v else v
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        if v is not None:
            if len(v) < 10:
                raise ValueError('La dirección debe tener al menos 10 caracteres')
            if len(v) > 200:
                raise ValueError('La dirección no puede tener más de 200 caracteres')
        return v.strip() if v else v
    
    def model_post_init(self, __context):
        """Valida que al menos un campo sea proporcionado después de la inicialización."""
        fields_to_check = [
            self.account_number, self.account_type, self.customer_name, 
            self.document_type, self.document_number,
            self.phone, self.email, self.address, self.amount
        ]
        if all(field is None for field in fields_to_check):
            raise ValueError('Debe proporcionar al menos un campo para actualizar')

class AccountResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra = {
            "example": {
                "id": "60a7e0e7a1b2c3d4e5f6a7b8",
                "account_number": "ACC-001",
                "account_type": "savings",
                "customer_name": "Juan Pérez García",
                "document_type": "CC",
                "document_number": "12345678",
                "phone": "+57 300 123 4567",
                "email": "juan.perez@email.com",
                "address": "Calle 123 #45-67, Bogotá",
                "balance": 1500.50
            }
        }
    )
    
    id: str
    account_number: str
    account_type: str
    customer_name: str
    document_type: str
    document_number: str
    phone: str
    email: str
    address: str
    balance: float
