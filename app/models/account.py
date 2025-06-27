from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Account(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    id: Optional[str] = Field(alias="_id", default=None)
    account_number: str = Field(..., min_length=3, max_length=50)
    account_type: str = Field(..., min_length=3, max_length=20)
    customer_name: str = Field(..., min_length=3, max_length=100)
    document_type: str = Field(..., min_length=2, max_length=10)
    document_number: str = Field(..., min_length=3, max_length=20)
    phone: str = Field(..., min_length=7, max_length=20)
    email: str = Field(..., min_length=5, max_length=100)
    address: str = Field(..., min_length=10, max_length=200)
    balance: float = Field(default=0.0, ge=0.0)
