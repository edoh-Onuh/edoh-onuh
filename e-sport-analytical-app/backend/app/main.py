from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

# ✅ Relative imports — correct for package structure
from .routers import matches, player_stats, predict, heatmap
# Temporarily disable live_data import to debug
# from .routers import live_data
from .models import Base
from .database import engine

# Create tables if they don't exist
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")

app = FastAPI(title="E-sport Analytics API")

# --- CORS Configuration for frontend dev ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global error handler ---
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal database error occurred."},
    )

# --- Include API routes ---
app.include_router(matches.router, tags=["Matches"])
app.include_router(player_stats.router, tags=["Player Stats"])
app.include_router(predict.router, tags=["Predictions"])
app.include_router(heatmap.router, tags=["Heatmaps"])
# Temporarily disable live_data router to debug
# app.include_router(live_data.router, tags=["Live Data"])

# Simple live data router for testing
live_router = APIRouter(prefix="/api/esport/live", tags=["Live Data"])

@live_router.get("/status")
async def get_live_status():
    return {
        "apis_available": [
            {"name": "HLTV", "game": "CS:GO", "status": "active"},
            {"name": "OpenDota", "game": "Dota 2", "status": "active"}
        ],
        "last_sync": datetime.now().isoformat(),
        "cache_status": {
            "matches_cached": 5,
            "players_cached": 10,
            "last_cache_update": datetime.now().isoformat()
        },
        "service_status": "operational"
    }

@live_router.get("/matches/live")
async def get_live_matches():
    return [
        {
            "id": f"match_{i}",
            "team1": f"Team Alpha {i}",
            "team2": f"Team Beta {i}",
            "game": "csgo",
            "status": "live" if i < 3 else "upcoming",
            "score": {"team1": 16 if i < 3 else 0, "team2": 14 if i < 3 else 0},
            "tournament": f"Championship {i}",
            "start_time": (datetime.now() + timedelta(hours=i)).isoformat()
        }
        for i in range(10)
    ]

@live_router.get("/players/live")
async def get_live_players():
    return [
        {
            "id": f"player_{i}",
            "player_name": f"Pro Player {i}",
            "game": "csgo",
            "rating": round(1.0 + (i * 0.1), 2),
            "kills": 25 + i,
            "deaths": 15 + i,
            "assists": 10 + i,
            "kda": round((25 + i + 10 + i) / max(15 + i, 1), 2),
            "team": f"Team {chr(65 + i)}",
            "last_match": (datetime.now() - timedelta(hours=i)).isoformat()
        }
        for i in range(10)
    ]

@live_router.get("/tournaments")
async def get_live_tournaments():
    return [
        {
            "id": f"tournament_{i}",
            "name": f"Championship Series {i}",
            "game": "csgo",
            "status": "upcoming",
            "start_date": (datetime.now() + timedelta(days=i)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=i+7)).isoformat(),
            "prize_pool": f"${(i+1) * 50000}",
            "teams": (i + 1) * 8,
            "organizer": f"ESL Gaming {i}",
            "location": "Online" if i % 2 == 0 else f"City {i}"
        }
        for i in range(5)
    ]

@live_router.get("/analytics/trends")
async def get_trending_analytics():
    return {
        "top_teams": [
            {"name": "Astralis", "wins": 15, "trend": "up"},
            {"name": "NAVI", "wins": 14, "trend": "stable"},
            {"name": "G2 Esports", "wins": 12, "trend": "down"}
        ],
        "top_players": [
            {"name": "s1mple", "rating": 1.35, "game": "csgo"},
            {"name": "ZywOo", "rating": 1.32, "game": "csgo"},
            {"name": "device", "rating": 1.28, "game": "csgo"}
        ],
        "match_frequency": {
            "total_matches_today": 45,
            "csgo": 20,
            "valorant": 15,
            "dota2": 10
        },
        "tournament_activity": {
            "active_tournaments": 8,
            "upcoming_tournaments": 12,
            "total_prize_pool": "$2,500,000"
        },
        "timeframe": "24h",
        "game_filter": None,
        "last_updated": datetime.now().isoformat()
    }

@live_router.get("/games/supported")
async def get_supported_games():
    return {
        "games": [
            {
                "name": "Counter-Strike: Global Offensive",
                "code": "csgo",
                "data_sources": ["HLTV", "FACEIT", "Steam"],
                "available_data": ["matches", "player_stats", "tournaments", "team_rankings"]
            },
            {
                "name": "Valorant",
                "code": "valorant",
                "data_sources": ["Riot Games API", "FACEIT"],
                "available_data": ["matches", "leaderboard", "tournaments"]
            },
            {
                "name": "Dota 2",
                "code": "dota2",
                "data_sources": ["OpenDota", "Steam"],
                "available_data": ["pro_matches", "player_stats", "leaderboard"]
            }
        ],
        "total_games": 3,
        "api_keys_required": ["Riot Games", "FACEIT", "Steam"],
        "free_apis": ["HLTV", "OpenDota"]
    }

app.include_router(live_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-sport Analytics API"}
