from typing import Annotated


from fastapi import Depends,FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import DeviceCreate, DeviceResponse, DeviceUpdate
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select

from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()




DbSession = Annoted[Session, Depends(get_db)]

@app.get("/", include_in_schema=False)
@app.get("/api/device", response_model=list[DeviceResponse])
def get_devices(db: DbSession):
    return dbscalars(select(models.Device)).all()


#Create device
@app.post(
    "/api/device", 
    response_model=DeviceResponse, status_code=status.HTTP_201_CREATED
)
def create_device(device: DeviceCreate, db: DbSession):
    if db.get(models.Device, device.serial_number):
        raise HTTPException(status_code=409, detail="A device with the serial number exiswts")
    new_device= models.Device(**device.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device



#Find device
@app.get("/api/device/{serial_number}", response_model=DeviceResponse)
def get_device(serial_number: str, db: DbSession):
    device = db.get(models.Device, serial_number)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="device not found")
    return device


#Put Device
@app.put("/api/device/{serial_number}", response_model=DeviceResponse)
def put_device(serial_number: str, update: DeviceUpdate, db:DbSession):
    device = db.get(models.Device, serial_number)
    if not device:
          raise HTTPException(status_code=404, detail="Device not found")
    for field, value in update.model_dump(exclude_unset=True).items():
          setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device
    


#Delete device
@app.delete("/api/device/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(serial_number: str, db: DbSession):
    device = db.get(models.Device, serial_number)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")    
    db.delete(device)
    db.commit
    


#RequestValidationHandler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return 
