from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserCreate(BaseModel):
    fullname: str = Field(min_length=3)
    email: EmailStr
    username: str = Field(min_length=6)
    password: str = Field(min_length=6)
    
class UserUpdating(BaseModel):
    # name: str | None = Field(default=None, min_length=3)
    
    fullname: str | None = Field(min_length=3)
    email: str | None = EmailStr
    username: str | None = Field(min_length=6)
    password: str | None = Field(min_length=6)
    

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fullname: str
    email: EmailStr
    username: str
