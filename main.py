from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Stand, Offer
from schemas import StandSchema
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