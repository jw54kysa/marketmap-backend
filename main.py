from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Stand, Offer, Device, DeviceActivation
from schemas import StandSchema, DeviceInitSchema, DeviceInitResponseSchema, DeviceResponsesSchema
from typing import List
from fastapi.staticfiles import StaticFiles

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Mount a folder to serve images
app.mount("/images", StaticFiles(directory="data/images"), name="images")

# SQLAdmin setup
admin = Admin(app=app, engine=engine, title="Stände Admin")

# Admin view for Stand
class StandAdmin(ModelView, model=Stand):
    column_list = ["id", "name", "offers", "icon", "type", "info", "open_time", "close_time", "lat", "lng"]
    can_create = True
    can_edit = True
    can_delete = True

class OfferAdmin(ModelView, model=Offer):
    column_list = ["id", "name", "price", "stand_id"]
    can_create = True
    can_edit = True
    can_delete = True

# Register admin view
admin.add_view(StandAdmin)
admin.add_view(OfferAdmin)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# STATUS
@app.get("/api/status")
def get_status(db: Session = Depends(get_db)):
    count = db.query(Stand).count()
    return JSONResponse(content={"stand_count": count})

# STANDS
# get list
@app.get("/api/stands", response_model=List[StandSchema])
def get_all_stands(db: Session = Depends(get_db)):
    stands = db.query(Stand).filter(Stand.is_active == True).all()
    return stands


# Tracker

@app.post("/api/tracker/activate", response_model=DeviceInitResponseSchema)
def register_device_activation(activation: DeviceInitSchema, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.uuid == activation.uuid).first()
    if not device:
        device = Device(uuid=activation.uuid)
        db.add(device)
        db.commit()
        db.refresh(device)

    new_activation = DeviceActivation(device_id=device.id)
    db.add(new_activation)
    db.commit()
    db.refresh(new_activation)

    return {"uuid": device.uuid, "markets": ["25_lpz_wm"]}


@app.get("/api/tracker/activations", response_model=List[DeviceResponsesSchema])
def get_all_device_activations(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    
    response = []
    for device in devices:
        timestamps = [activation.timestamp for activation in device.activations]
        response.append({"uuid": device.uuid, "activations": timestamps})
    
    return response