from pydantic import BaseModel, AnyHttpUrl

# Data Models
class URLObject(BaseModel):
    id: int
    longUrl: AnyHttpUrl
    shortUrl: AnyHttpUrl
    code: str

class URLPayload(BaseModel):
    url: AnyHttpUrl