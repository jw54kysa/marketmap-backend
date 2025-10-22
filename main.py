from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Stand, Offer, Device, DeviceActivation, DeviceStandRating
from schemas import *
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func

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
def get_all_stands(
    event: Optional[str] = Query(None, description="Event code to filter stands"),
    db: Session = Depends(get_db)
):
    query = db.query(Stand).filter(Stand.is_active == True)

    # Filter by city if provided
    if event:
        query = query.filter(Stand.event == event)

    stands = query.all()

    # Compute average rating for each stand
    stand_list = []
    for stand in stands:
        avg = db.query(func.avg(DeviceStandRating.rating)) \
                .filter(DeviceStandRating.stand_id == stand.id) \
                .scalar()
        stand.rating = float(avg) if avg is not None else None
        stand_list.append(stand)

    return stand_list


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


# Rating 

@app.post("/api/stands/rate")
def rate_stand(rating_data: RatingSchema, db: Session = Depends(get_db)):
    # Check or create device
    device = db.query(Device).filter(Device.uuid == rating_data.device_uuid).first()
    if not device:
        device = Device(uuid=rating_data.device_uuid)
        db.add(device)
        db.commit()
        db.refresh(device)
    
    # Check if stand exists
    stand = db.query(Stand).filter(Stand.id == rating_data.stand_id).first()
    if not stand:
        raise HTTPException(status_code=404, detail="Stand not found")
    
    # Check if a rating already exists
    existing_rating = db.query(DeviceStandRating).filter(
        DeviceStandRating.device_id == device.id,
        DeviceStandRating.stand_id == stand.id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating_data.rating  # update rating
    else:
        new_rating = DeviceStandRating(
            device_id=device.id,
            stand_id=stand.id,
            rating=rating_data.rating
        )
        db.add(new_rating)
    
    db.commit()
    return {"message": "Rating submitted successfully"}

@app.get("/api/stands/rating", response_model=DeviceStandRatingResponse)
def get_device_rating(device_uuid: str, stand_id: int, db: Session = Depends(get_db)):
    # Find device
    device = db.query(Device).filter(Device.uuid == device_uuid).first()
    if not device:
        return DeviceStandRatingResponse(
            device_uuid=device_uuid,
            stand_id=stand_id,
            rating=None
        )
    
    # Find stand
    stand = db.query(Stand).filter(Stand.id == stand_id).first()
    if not stand:
        return DeviceStandRatingResponse(
            device_uuid=device_uuid,
            stand_id=stand_id,
            rating=None
        )
    
    # Find rating
    rating_entry = db.query(DeviceStandRating).filter(
        DeviceStandRating.device_id == device.id,
        DeviceStandRating.stand_id == stand.id
    ).first()
    
    return DeviceStandRatingResponse(
        device_uuid=device_uuid,
        stand_id=stand_id,
        rating=rating_entry.rating if rating_entry else None
    )
