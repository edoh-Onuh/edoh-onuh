# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlayerStatBase(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=100)
    kills: int = Field(default=0, ge=0)
    deaths: int = Field(default=0, ge=0)
    assists: int = Field(default=0, ge=0)

class PlayerStat(PlayerStatBase):
    id: int
    match_id: Optional[int] = None
    kda_ratio: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    team_name: str = Field(..., min_length=1, max_length=100)
    opponent_name: str = Field(..., min_length=1, max_length=100)
    result: str = Field(..., pattern="^(win|loss|draw)$")

class Match(MatchBase):
    id: int
    match_date: Optional[datetime] = None
    score_team: Optional[int] = 0
    score_opponent: Optional[int] = 0
    game_mode: Optional[str] = None

    class Config:
        from_attributes = True

class PositionFrequencyBase(BaseModel):
    x: float
    y: float
    frequency: int = Field(default=1, ge=1)

class PositionFrequency(PositionFrequencyBase):
    id: int
    player_name: Optional[str] = None
    map_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True