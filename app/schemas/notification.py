from pydantic import BaseModel, Field


class DeviceTokenRequest(BaseModel):
    token: str = Field(min_length=1)
    platform: str = Field(default="android", min_length=1, max_length=20)
