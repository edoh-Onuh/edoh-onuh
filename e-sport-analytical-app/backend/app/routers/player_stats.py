# app/routers/player_stats.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from .. import schemas
from ..dependencies import get_db
from ..models import PlayerStat, Match

router = APIRouter(prefix="/api/esport/player-stats", tags=["player-stats"])

@router.get("/")
def read_player_stats(
    player_name: Optional[str] = Query(None, description="Filter by player name"),
    limit: int = Query(100, description="Maximum number of stats to return"),
    skip: int = Query(0, description="Number of stats to skip"),
    db: Session = Depends(get_db)
):
    """
    Retrieve player statistics with optional filtering and team information.
    """
    try:
        # Join PlayerStat with Match to get team information
        query = db.query(
            PlayerStat.id,
            PlayerStat.player_name,
            PlayerStat.kills,
            PlayerStat.deaths,
            PlayerStat.assists,
            PlayerStat.kda_ratio,
            PlayerStat.match_id,
            PlayerStat.created_at,
            Match.team_name,
            Match.match_date
        ).outerjoin(Match, PlayerStat.match_id == Match.id)
        
        if player_name:
            query = query.filter(PlayerStat.player_name.ilike(f"%{player_name}%"))
        
        results = query.order_by(desc(PlayerStat.created_at)).offset(skip).limit(limit).all()
        
        # Convert to list of dictionaries
        stats = []
        for result in results:
            stats.append({
                "id": result.id,
                "player_name": result.player_name,
                "team_name": result.team_name or "Unknown Team",
                "kills": result.kills,
                "deaths": result.deaths,
                "assists": result.assists,
                "kda_ratio": result.kda_ratio,
                "match_id": result.match_id,
                "created_at": result.created_at,
                "match_date": result.match_date
            })
        
        # Debug print
        print(f"🔍 DEBUG: Found {len(stats)} player stats for '{player_name}' from database")
        if stats:
            print(f"🔍 DEBUG: First player: {stats[0]['player_name']} ({stats[0]['team_name']})")
        
        return stats
    
    except Exception as e:
        print(f"❌ DEBUG: Error in read_player_stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving player stats: {str(e)}")

@router.get("/summary")
def get_player_summary(db: Session = Depends(get_db)):
    """
    Get aggregated player statistics summary.
    """
    try:
        summary = db.query(
            PlayerStat.player_name,
            func.sum(PlayerStat.kills).label('total_kills'),
            func.sum(PlayerStat.deaths).label('total_deaths'),
            func.sum(PlayerStat.assists).label('total_assists'),
            func.avg(PlayerStat.kda_ratio).label('avg_kda'),
            func.count(PlayerStat.id).label('games_played')
        ).group_by(PlayerStat.player_name).all()
        
        return [
            {
                "player_name": stat.player_name,
                "total_kills": stat.total_kills or 0,
                "total_deaths": stat.total_deaths or 0,
                "total_assists": stat.total_assists or 0,
                "avg_kda": round(float(stat.avg_kda or 0), 2),
                "games_played": stat.games_played
            }
            for stat in summary
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving player summary: {str(e)}")