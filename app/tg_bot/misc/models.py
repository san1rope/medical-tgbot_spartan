from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict, EmailStr


class ConsultantForm(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    name: Optional[str] = None
    about_yourself: Optional[str] = None
    country: Optional[str] = None
    locality: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("name", "about_yourself", "locality")
    @classmethod
    def check_isdigit(cls, value: str):
        if value is not None and value.isdigit():
            raise ValueError("isdigit true")

        return value
