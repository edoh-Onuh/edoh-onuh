# app/routers/matches.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from .. import schemas
from ..dependencies import get_db
from ..models import Match

router = APIRouter(prefix="/api/esport/matches", tags=["matches"])

@router.get("/")
def read_matches(
    team: Optional[str] = Query(None, description="Filter matches by team name"),
    limit: int = Query(100, description="Maximum number of matches to return"),
    skip: int = Query(0, description="Number of matches to skip"),
    db: Session = Depends(get_db)
):
    """
    Retrieve matches with optional filtering by team name.
    """
    try:
        query = db.query(Match)
        
        if team:
            query = query.filter(
                (Match.team_name.ilike(f"%{team}%")) | 
                (Match.opponent_name.ilike(f"%{team}%"))
            )
        
        matches = query.order_by(desc(Match.match_date)).offset(skip).limit(limit).all()
        
        # Convert to list of dictionaries with proper field names for frontend
        match_list = []
        for match in matches:
            match_list.append({
                "id": match.id,
                "team_name": match.team_name,
                "opponent_name": match.opponent_name,
                "match_date": match.match_date.strftime("%Y-%m-%d") if match.match_date else None,
                "score_team": match.score_team,
                "score_opponent": match.score_opponent,
                "result": match.result,
                "tournament": match.game_mode or "Tournament"  # Use game_mode as tournament
            })
        
        # Debug print to see what we're getting
        print(f"🔍 DEBUG: Found {len(match_list)} matches for team '{team}' from database")
        if match_list:
            print(f"🔍 DEBUG: First match: {match_list[0]['team_name']} vs {match_list[0]['opponent_name']}")
        
        return match_list
    
    except Exception as e:
        print(f"❌ DEBUG: Error in read_matches: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving matches: {str(e)}")

@router.get("/{match_id}", response_model=schemas.Match)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """
    Get a specific match by ID.
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match