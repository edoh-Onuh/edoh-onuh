from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PlayerStat

router = APIRouter(prefix="/api/esport/player-stats")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_player_stats(db: Session = Depends(get_db)):
    return db.query(PlayerStat).all()
