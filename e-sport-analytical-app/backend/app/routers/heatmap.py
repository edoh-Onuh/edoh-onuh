# app/routers/heatmap.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies import get_db
from ..models import PositionFrequency

router = APIRouter(prefix="/api/esport/position-heatmap", tags=["heatmap"])

@router.get("/")
def read_heatmap(
    player_name: Optional[str] = Query(None, description="Filter by player name"),
    team: Optional[str] = Query(None, description="Filter by team name"),
    map_name: Optional[str] = Query(None, description="Filter by map name"),
    min_frequency: int = Query(1, description="Minimum frequency threshold"),
    db: Session = Depends(get_db)
):
    """
    Retrieve position frequency data for heatmap generation.
    """
    try:
        query = db.query(PositionFrequency).filter(PositionFrequency.frequency >= min_frequency)
        
        if player_name:
            query = query.filter(PositionFrequency.player_name.ilike(f"%{player_name}%"))
        
        if team:
            # For team filtering, we'd need to join with player stats or matches
            # For now, just filter by common team player names
            team_players = ["s1mple", "electronic"] if "navi" in team.lower() else []
            if "tsm" in team.lower():
                team_players = ["FalleN", "Twistzz"]
            elif "astralis" in team.lower():
                team_players = ["device", "ropz"]
            elif "vitality" in team.lower():
                team_players = ["ZywOo", "MICHU"]
            
            if team_players:
                query = query.filter(PositionFrequency.player_name.in_(team_players))
        
        if map_name:
            query = query.filter(PositionFrequency.map_name.ilike(f"%{map_name}%"))
        
        positions = query.all()
        
        # Convert to proper format
        heatmap_data = [
            {
                "x": pos.x,
                "y": pos.y,
                "frequency": pos.frequency,
                "player_name": pos.player_name,
                "map_name": pos.map_name
            }
            for pos in positions
        ]
        
        print(f"🔍 DEBUG: Found {len(heatmap_data)} position points for player '{player_name}', team '{team}'")
        
        return {"data": heatmap_data}
    
    except Exception as e:
        print(f"❌ DEBUG: Error in read_heatmap: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving heatmap data: {str(e)}")