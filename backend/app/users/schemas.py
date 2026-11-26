from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_special: bool

    model_config = ConfigDict(from_attributes=True)