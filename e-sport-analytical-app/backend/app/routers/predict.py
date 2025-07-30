# app/routers/predict.py
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..dependencies import get_db
from ..models import Match, PlayerStat

router = APIRouter(prefix="/api/esport/predict", tags=["predictions"])

@router.get("/")
def predict_outcome(
    team: str = Query(..., description="Team name for prediction"),
    db: Session = Depends(get_db)
):
    """
    Predict match outcome based on historical data.
    Simple prediction algorithm based on win rate and recent performance.
    """
    try:
        # Get team's historical performance
        total_matches = db.query(Match).filter(
            (Match.team_name.ilike(f"%{team}%")) | 
            (Match.opponent_name.ilike(f"%{team}%"))
        ).count()
        
        if total_matches == 0:
            return {
                "team": team,
                "win_probability": 0.5,
                "confidence": "low",
                "message": "No historical data available for this team",
                "matches_analyzed": 0
            }
        
        # Calculate win rate
        wins = db.query(Match).filter(
            Match.team_name.ilike(f"%{team}%"),
            Match.result == "win"
        ).count()
        
        win_rate = wins / total_matches if total_matches > 0 else 0.5
        
        # Get recent performance (last 10 matches)
        recent_matches = db.query(Match).filter(
            (Match.team_name.ilike(f"%{team}%")) | 
            (Match.opponent_name.ilike(f"%{team}%"))
        ).order_by(Match.match_date.desc()).limit(10).all()
        
        recent_wins = sum(1 for match in recent_matches 
                         if match.team_name.lower() == team.lower() and match.result == "win")
        recent_win_rate = recent_wins / len(recent_matches) if recent_matches else 0.5
        
        # Weighted prediction (70% historical, 30% recent)
        prediction = (win_rate * 0.7) + (recent_win_rate * 0.3)
        
        # Determine confidence level
        confidence = "high" if total_matches >= 20 else "medium" if total_matches >= 10 else "low"
        
        return {
            "team": team,
            "win_probability": round(prediction, 3),
            "confidence": confidence,
            "historical_win_rate": round(win_rate, 3),
            "recent_win_rate": round(recent_win_rate, 3),
            "matches_analyzed": total_matches,
            "recent_matches_analyzed": len(recent_matches)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating prediction: {str(e)}")