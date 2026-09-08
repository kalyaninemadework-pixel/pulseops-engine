from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', description='User email address')
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: Optional[str] = 'engineer'

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    username: Optional[str] = None
