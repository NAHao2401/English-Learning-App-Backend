from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)


class ChangePasswordResponse(BaseModel):
    message: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    user: UserResponse