from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(type="string")

class Account(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    account_holder_name: str = Field(..., min_length=3, max_length=100)
    balance: float = Field(default=0.0, ge=0.0)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True # Permite el tipo PyObjectId