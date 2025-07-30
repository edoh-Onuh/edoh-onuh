# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .database import engine

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(100), nullable=False)
    opponent_name = Column(String(100), nullable=False)
    result = Column(String(20), nullable=False)  # 'win', 'loss', 'draw'
    match_date = Column(DateTime, default=func.now())
    score_team = Column(Integer, default=0)
    score_opponent = Column(Integer, default=0)
    game_mode = Column(String(50))
    
    def __repr__(self):
        return f"<Match(team='{self.team_name}', opponent='{self.opponent_name}', result='{self.result}')>"

class PlayerStat(Base):
    __tablename__ = "player_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(100), nullable=False, index=True)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    match_id = Column(Integer)  # Foreign key to matches
    kda_ratio = Column(Float)  # Calculated field
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<PlayerStat(player='{self.player_name}', K/D/A={self.kills}/{self.deaths}/{self.assists})>"

class PositionFrequency(Base):
    __tablename__ = "position_frequency"
    
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    frequency = Column(Integer, default=1)
    player_name = Column(String(100))
    map_name = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<PositionFrequency(x={self.x}, y={self.y}, freq={self.frequency})>"

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print(" Database tables created successfully!")
except Exception as e:
    print(f" Error creating tables: {e}")