from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Stand

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# SQLAdmin setup
admin = Admin(app=app, engine=engine, title="Stände Admin")

# Admin view for Stand
class StandAdmin(ModelView, model=Stand):
    column_list = ["id", "name", "icon", "type", "info", "open_time", "close_time", "lat", "lng"]
    can_create = True
    can_edit = True
    can_delete = True

# Register admin view
admin.add_view(StandAdmin)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to fetch all stands
@app.get("/api/stands")
def get_all_stands():
    db: Session = next(get_db())
    stands = db.query(Stand).all()
    result = [
        {
            "id": s.id,
            "name": s.name,
            "icon": s.icon,
            "type": s.type,
            "info": s.info,
            "open_time": s.open_time,
            "close_time": s.close_time,
            "lat": s.lat,
            "lng": s.lng
        }
        for s in stands
    ]
    return JSONResponse(content=result)

@app.get("/api/status")
def get_status():
    db: Session = next(get_db())
    count = db.query(Stand).count()
    return JSONResponse(content={"stand_count": count})