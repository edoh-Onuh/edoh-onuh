# app/services/matches.py
from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List, Optional

def get_matches(db: Session, team_name: Optional[str] = None) -> List[schemas.Match]:
    query = db.query(models.Match)
    if team_name:
        query = query.filter(models.Match.team_name.ilike(f"%{team_name}%"))
    return query.all()