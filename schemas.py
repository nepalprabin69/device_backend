from pydantic import BaseModel, ConfigDict, Field

class DeviceBase(BaseModel):
    serial_number: str = Field(min_length=1, max_length=10)
    lat: int = Field(ge=-90,le=90)
    long: int = Field(ge=-180,le=180)
    type: str = Field(min_length=1, max_length=50)
    version: int = Field(ge=0)
    is_active: bool = True


class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    lat: float | None = Field(default=None, ge=-90, le=90)
    long: float | None = Field(default=None, ge=-180, le=180)
    type: str | None = Field(default=None, min_length=1, max_length=50)
    version: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    pass

   
    
     