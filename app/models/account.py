from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Account(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    id: Optional[str] = Field(alias="_id", default=None)
    account_holder_name: str = Field(..., min_length=3, max_length=100)
    balance: float = Field(default=0.0, ge=0.0)
