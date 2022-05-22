from pydantic import BaseModel, ValidationError, Field, validator

class Settings(BaseModel): 
    volume: int = Field(alias="volume")
    music: str = Field(alias="music")
    language: str = Field(alias="language")
