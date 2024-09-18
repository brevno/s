from typing import Optional

from pydantic import BaseModel, HttpUrl

class URLInput(BaseModel):
    url: HttpUrl
    expiration_hrs: Optional[int]  = 0

class CreatedResponse(BaseModel):
    short_url: str
