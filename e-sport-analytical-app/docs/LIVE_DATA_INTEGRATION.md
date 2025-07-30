# 🌐 Real-World E-Sports API Integration Guide

## Overview

Your E-Sport Analytics Platform now supports **real-world data integration** from multiple popular e-sports APIs! This guide will help you set up and use live data from CS:GO, Valorant, and Dota 2.

## 🎮 Supported Games & Data Sources

### Counter-Strike: Global Offensive (CS:GO)
- **HLTV API** (Free) - Match results, player statistics, team rankings
- **FACEIT API** (Requires key) - Tournament data, player stats
- **Steam Web API** (Requires key) - Player profiles, game statistics

### Valorant
- **Riot Games API** (Requires key) - Match history, leaderboards, player stats
- **FACEIT API** (Requires key) - Tournament data

### Dota 2
- **OpenDota API** (Free) - Professional matches, player statistics
- **Steam Web API** (Requires key) - Player profiles, match data

## 🚀 Quick Setup

### 1. Run the Setup Script
```bash
cd backend
python setup_apis.py
```

This interactive script will:
- Create your `.env` file
- Guide you through API key configuration
- Test all API connections
- Install required dependencies

### 2. Get API Keys (Optional but Recommended)

#### Riot Games API (Valorant, League of Legends)
1. Visit: https://developer.riotgames.com/
2. Create an account and generate a development key
3. Add to `.env`: `RIOT_API_KEY=RGAPI-your-key-here`

#### Steam Web API (CS:GO, Dota 2)
1. Visit: https://steamcommunity.com/dev/apikey
2. Generate your API key
3. Add to `.env`: `STEAM_API_KEY=your-key-here`

#### FACEIT API (Multiple games, tournaments)
1. Visit: https://developers.faceit.com/
2. Create an application and get your API key
3. Add to `.env`: `FACEIT_API_KEY=your-key-here`

### 3. Start the Enhanced Backend
```bash
cd backend
python run_server.py
```

### 4. Use Live Data in Frontend
- Open your dashboard at http://localhost:3000
- Use the **"Live Data Toggle"** to switch between sample and real data
- Select your preferred game and search for teams/players

## 📡 New API Endpoints

### Live Matches
```http
GET /api/esport/live/matches/live?game=csgo&limit=50
GET /api/esport/live/matches/live?game=valorant
GET /api/esport/live/matches/live?game=dota2
```

### Live Player Statistics
```http
GET /api/esport/live/players/live?game=csgo&limit=50
GET /api/esport/live/players/live?game=valorant
GET /api/esport/live/players/live?player_id=specific_player
```

### Tournament Data
```http
GET /api/esport/live/tournaments?game=csgo&status=upcoming
GET /api/esport/live/tournaments?game=valorant&status=live
```

### API Status & Health
```http
GET /api/esport/live/status
GET /api/esport/live/health
GET /api/esport/live/games/supported
```

### Trending Analytics
```http
GET /api/esport/live/analytics/trends?game=csgo&timeframe=24h
GET /api/esport/live/analytics/trends?timeframe=7d
```

### Data Synchronization
```http
POST /api/esport/live/sync?force=true
```

## 🎯 Frontend Integration

### Using the Live Data Toggle
The frontend now includes a `LiveDataToggle` component that allows users to:
- Switch between sample data and live data
- View API status and supported games
- Trigger data synchronization
- See cache status and last update times

### API Service Functions
```javascript
import * as api from './services/api';

// Get live CS:GO matches
const csgoMatches = await api.getCSGOMatches(50);

// Get Valorant leaderboard
const valorantPlayers = await api.getValorantLeaderboard(100);

// Get Dota 2 player stats
const dotaStats = await api.getDota2PlayerStats('account_id');

// Get all dashboard data (smart switching between sample/live)
const dashboardData = await api.getDashboardData({
  useLiveData: true,
  game: 'csgo',
  team: 'Astralis',
  limit: 50
});
```

## 🔧 Configuration Options

### Environment Variables (.env)
```env
# External APIs
RIOT_API_KEY=RGAPI-your-riot-api-key
STEAM_API_KEY=your-steam-api-key
FACEIT_API_KEY=your-faceit-api-key

# API Settings
API_CACHE_TTL=300  # Cache for 5 minutes
API_REQUEST_TIMEOUT=30
MAX_CONCURRENT_REQUESTS=10

# Data Sync
DATA_SYNC_INTERVAL=300  # Sync every 5 minutes
AUTO_SYNC_ON_STARTUP=true
```

### Rate Limiting
The platform automatically handles rate limits:
- **HLTV**: 100 requests/minute (free)
- **OpenDota**: 60 requests/minute (free)
- **Riot Games**: 100 requests/2 minutes
- **FACEIT**: 1000 requests/minute
- **Steam**: 100,000 requests/day

## 📊 Data Examples

### CS:GO Match Data
```json
{
  "match_id": "2372123",
  "team1": "Astralis",
  "team2": "NAVI",
  "score1": 16,
  "score2": 12,
  "date": "2025-01-20T14:30:00Z",
  "event": "IEM Katowice 2025",
  "map": "de_dust2",
  "game": "csgo"
}
```

### Valorant Player Data
```json
{
  "player_id": "player123",
  "player_name": "TenZ",
  "player_tag": "TEN",
  "rank": 1,
  "ranked_rating": 456,
  "number_of_wins": 89,
  "game": "valorant"
}
```

### Dota 2 Match Data
```json
{
  "match_id": 7234567890,
  "radiant_team": "Team Secret",
  "dire_team": "OG",
  "radiant_score": 25,
  "dire_score": 18,
  "radiant_win": true,
  "duration": 2847,
  "league_name": "The International 2025",
  "game": "dota2"
}
```

## 🛠️ Troubleshooting

### Common Issues

#### "Live APIs not available"
- Check your `.env` file has API keys
- Run `python setup_apis.py` to test connections
- Restart the backend server

#### "Rate limit exceeded"
- Wait for the rate limit to reset
- Consider implementing Redis for better caching
- Use `force_refresh=false` to use cached data

#### "API key invalid"
- Verify your API keys are correct
- Check if your API key has expired
- Ensure proper permissions for your keys

### Testing API Connections
```bash
cd backend
python setup_apis.py  # Run setup and test
python test_api.py    # Test sample data endpoints
```

### Checking Live Data Status
Visit: http://127.0.0.1:8000/api/esport/live/status

## 🚀 Advanced Features

### Background Data Sync
The platform automatically syncs data every 5 minutes:
```python
# Trigger manual sync
POST /api/esport/live/sync?force=true

# Check sync status
GET /api/esport/live/status
```

### Multi-Game Analytics
```javascript
// Get trending data across all games
const trends = await api.getTrendingAnalytics(null, '24h');

// Game-specific trends
const csgoTrends = await api.getTrendingAnalytics('csgo', '7d');
```

### Smart Caching
- 5-minute cache for match data
- 10-minute cache for player statistics
- 15-minute cache for tournament data
- Automatic cache invalidation on sync

## 📈 Performance Tips

1. **Use Caching**: Don't set `force_refresh=true` unless necessary
2. **Batch Requests**: Use the unified dashboard API when possible
3. **Monitor Rate Limits**: Check API status regularly
4. **Background Sync**: Let automatic sync handle routine updates

## 🎉 What's Next?

Your platform now supports:
- ✅ Real-time match data from 3+ games
- ✅ Live player statistics and rankings
- ✅ Tournament schedules and results
- ✅ Trending analytics and insights
- ✅ Smart caching and rate limiting
- ✅ Background data synchronization

Enjoy exploring real-world e-sports data! 🎮📊
