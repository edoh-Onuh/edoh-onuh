# API Documentation

## Base URL
```
http://127.0.0.1:8000/api/esport
```

## Endpoints

### Matches

#### GET /matches/
Get all matches or filter by team name.

**Parameters:**
- `team` (optional): Filter matches by team name
- `limit` (optional): Maximum number of matches to return (default: 100)
- `skip` (optional): Number of matches to skip (default: 0)

**Example:**
```bash
GET /api/esport/matches/?team=TSM&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "team_name": "TSM",
    "opponent_name": "Astralis",
    "match_date": "2025-07-23T10:30:00",
    "score_team": 16,
    "score_opponent": 12,
    "result": "win",
    "game_mode": "Competitive"
  }
]
```

#### GET /matches/{match_id}
Get a specific match by ID.

**Parameters:**
- `match_id`: Match ID

**Response:**
```json
{
  "id": 1,
  "team_name": "TSM",
  "opponent_name": "Astralis",
  "match_date": "2025-07-23T10:30:00",
  "score_team": 16,
  "score_opponent": 12,
  "result": "win",
  "game_mode": "Competitive"
}
```

### Player Statistics

#### GET /player-stats/
Get all player statistics or filter by player name.

**Parameters:**
- `player_name` (optional): Filter by player name
- `limit` (optional): Maximum number of records (default: 100)
- `skip` (optional): Number of records to skip (default: 0)

**Example:**
```bash
GET /api/esport/player-stats/?player_name=device
```

**Response:**
```json
[
  {
    "id": 1,
    "player_name": "device",
    "match_id": 1,
    "kills": 24,
    "deaths": 12,
    "assists": 8,
    "kda_ratio": 2.67,
    "created_at": "2025-07-23T10:30:00"
  }
]
```

### Position Heatmap

#### GET /position-heatmap/
Get position frequency data for heatmap visualization.

**Response:**
```json
[
  {
    "id": 1,
    "position": "A Site",
    "frequency": 45
  },
  {
    "id": 2,
    "position": "B Site", 
    "frequency": 32
  }
]
```

### Predictions

#### GET /predict/
Get match predictions based on team performance.

**Parameters:**
- `team` (optional): Team name for prediction

**Example:**
```bash
GET /api/esport/predict/?team=TSM
```

**Response:**
```json
{
  "team": "TSM",
  "win_probability": 0.72,
  "confidence": 0.85,
  "factors": {
    "recent_form": 0.8,
    "head_to_head": 0.65,
    "player_performance": 0.75
  }
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include a detail message:
```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

Currently, no rate limiting is implemented, but it's recommended to implement it in production environments.
