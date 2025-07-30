# models.py
from sqlalchemy import Column, Integer, String, Float
from database import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(50))
    opponent_name = Column(String(50))
    result = Column(String(10))

class PlayerStat(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(50))
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)

class PositionFrequency(Base):
    __tablename__ = "position_frequency"
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    frequency = Column(Integer)

Base.metadata.create_all(bind=engine)

# routers/matches.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Match

router = APIRouter(prefix="/api/esport/matches")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()

# routers/player_stats.py
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

# routers/heatmap.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PositionFrequency

router = APIRouter(prefix="/api/esport/position-heatmap")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_heatmap(db: Session = Depends(get_db)):
    return db.query(PositionFrequency).all()

# routers/predict.py
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/esport/predict")

@router.get("/")
def predict_outcome(team: str = Query(...)):
    return {"team": team, "win_probability": 0.65}

# Azure Key Vault integration (database.py example)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://your-key-vault-name.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

db_user = client.get_secret("db-user").value
db_pass = client.get_secret("db-password").value
db_host = client.get_secret("db-host").value
db_name = client.get_secret("db-name").value

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# GitHub repo scaffold (README.md suggestion)
# Esport Data Analysis Backend
#This repo contains:
#- FastAPI backend
#- React frontend
#- Docker / Helm / Azure pipelines
#- Azure Key Vault integration

## Quickstart
#```bash
#docker build -t esport-backend .
#docker run -p 80:80 esport-backend
#```

## Azure Deploy
#Use provided Helm chart and pipeline YAML files.
