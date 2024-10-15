from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)
    full_amount: conint(gt=0)

    class Config:
        extra = Extra.forbid

    @validator("full_amount")
    def validate_full_amount(cls, value):
        if value < 0:
            raise ValueError("full amount не может быть отрицательным")
        return value


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: Optional[conint(gt=0)]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(..., ge=0)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True

    @validator("invested_amount")
    def validate_invested_amount(cls, value):
        if value < 0:
            raise ValueError("invested amount не может быть отрицательным")
        return value
