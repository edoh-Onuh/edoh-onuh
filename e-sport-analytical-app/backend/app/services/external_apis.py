# app/services/external_apis.py
"""
External API integrations for real-world e-sports data
Supports multiple gaming platforms and tournaments
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ESportsAPIClient:
    """Unified client for multiple e-sports APIs"""
    
    def __init__(self):
        self.session = None
        
        # API Configuration
        self.apis = {
            'riot_games': {
                'base_url': 'https://americas.api.riotgames.com',
                'api_key': os.getenv('RIOT_API_KEY'),
                'rate_limit': 100,  # requests per 2 minutes
                'games': ['valorant', 'league_of_legends']
            },
            'steam': {
                'base_url': 'https://api.steampowered.com',
                'api_key': os.getenv('STEAM_API_KEY'),
                'rate_limit': 100000,  # requests per day
                'games': ['csgo', 'dota2']
            },
            'faceit': {
                'base_url': 'https://open-api.faceit.com/data/v4',
                'api_key': os.getenv('FACEIT_API_KEY'),
                'rate_limit': 1000,  # requests per minute
                'games': ['csgo', 'valorant']
            },
            'opendota': {
                'base_url': 'https://api.opendota.com/api',
                'api_key': None,  # Free tier
                'rate_limit': 60,  # requests per minute
                'games': ['dota2']
            },
            'hltv': {
                'base_url': 'https://hltv-api.vercel.app/api',
                'api_key': None,  # Free tier
                'rate_limit': 100,  # requests per minute
                'games': ['csgo']
            }
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, api_name: str, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to external API"""
        api_config = self.apis[api_name]
        url = f"{api_config['base_url']}{endpoint}"
        
        headers = {'Accept': 'application/json'}
        if api_config['api_key']:
            if api_name == 'riot_games':
                headers['X-Riot-Token'] = api_config['api_key']
            elif api_name == 'steam':
                params = params or {}
                params['key'] = api_config['api_key']
            elif api_name == 'faceit':
                headers['Authorization'] = f"Bearer {api_config['api_key']}"
        
        try:
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"API {api_name} returned status {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error fetching from {api_name}: {e}")
            return {}
    
    # ===============================
    # CS:GO / CS2 Data Integration
    # ===============================
    
    async def get_csgo_matches(self, limit: int = 50) -> List[Dict]:
        """Fetch recent CS:GO matches from HLTV"""
        endpoint = "/matches"
        data = await self._make_request('hltv', endpoint)
        
        matches = []
        for match in data.get('matches', [])[:limit]:
            matches.append({
                'match_id': match.get('id'),
                'team1': match.get('team1', {}).get('name'),
                'team2': match.get('team2', {}).get('name'),
                'score1': match.get('result', {}).get('team1'),
                'score2': match.get('result', {}).get('team2'),
                'date': match.get('date'),
                'event': match.get('event', {}).get('name'),
                'map': match.get('maps', [{}])[0].get('name') if match.get('maps') else None,
                'game': 'csgo'
            })
        
        return matches
    
    async def get_csgo_player_stats(self, player_id: str = None) -> List[Dict]:
        """Fetch CS:GO player statistics"""
        if player_id:
            endpoint = f"/players/{player_id}/stats"
        else:
            endpoint = "/players/top"
        
        data = await self._make_request('hltv', endpoint)
        
        stats = []
        players = data.get('players', []) if not player_id else [data]
        
        for player in players:
            stats.append({
                'player_id': player.get('id'),
                'player_name': player.get('name'),
                'team': player.get('team', {}).get('name'),
                'rating': player.get('rating2'),
                'kills_per_round': player.get('killsPerRound'),
                'deaths_per_round': player.get('deathsPerRound'),
                'adr': player.get('adr'),  # Average Damage per Round
                'kast': player.get('kast'),  # Kill/Assist/Survive/Trade percentage
                'impact': player.get('impact'),
                'game': 'csgo'
            })
        
        return stats
    
    # ===============================
    # Valorant Data Integration
    # ===============================
    
    async def get_valorant_matches(self, region: str = 'americas') -> List[Dict]:
        """Fetch Valorant competitive matches"""
        endpoint = f"/val/match/v1/recent-matches/by-queue/competitive"
        data = await self._make_request('riot_games', endpoint)
        
        matches = []
        for match in data.get('matches', []):
            matches.append({
                'match_id': match.get('matchId'),
                'game_start': match.get('gameStartTimeMillis'),
                'game_length': match.get('gameLengthMillis'),
                'queue_id': match.get('queueId'),
                'map': match.get('mapId'),
                'season': match.get('seasonId'),
                'game': 'valorant'
            })
        
        return matches
    
    async def get_valorant_leaderboard(self, act_id: str = None) -> List[Dict]:
        """Fetch Valorant leaderboard data"""
        endpoint = f"/val/ranked/v1/leaderboards/by-act/{act_id or 'current'}"
        data = await self._make_request('riot_games', endpoint)
        
        players = []
        for player in data.get('players', []):
            players.append({
                'player_id': player.get('playerId'),
                'player_name': player.get('gameName'),
                'player_tag': player.get('tagLine'),
                'rank': player.get('leaderboardRank'),
                'ranked_rating': player.get('rankedRating'),
                'number_of_wins': player.get('numberOfWins'),
                'game': 'valorant'
            })
        
        return players
    
    # ===============================
    # Dota 2 Data Integration
    # ===============================
    
    async def get_dota2_matches(self, limit: int = 100) -> List[Dict]:
        """Fetch recent Dota 2 pro matches"""
        endpoint = "/proMatches"
        data = await self._make_request('opendota', endpoint)
        
        matches = []
        for match in data[:limit]:
            matches.append({
                'match_id': match.get('match_id'),
                'start_time': match.get('start_time'),
                'duration': match.get('duration'),
                'radiant_team': match.get('radiant_team', {}).get('name'),
                'dire_team': match.get('dire_team', {}).get('name'),
                'radiant_score': match.get('radiant_score'),
                'dire_score': match.get('dire_score'),
                'radiant_win': match.get('radiant_win'),
                'league_name': match.get('league', {}).get('name'),
                'game': 'dota2'
            })
        
        return matches
    
    async def get_dota2_player_stats(self, account_id: str = None) -> List[Dict]:
        """Fetch Dota 2 player statistics"""
        if account_id:
            endpoint = f"/players/{account_id}"
            data = await self._make_request('opendota', endpoint)
            return [self._format_dota2_player(data)]
        else:
            endpoint = "/players"
            data = await self._make_request('opendota', endpoint)
            return [self._format_dota2_player(player) for player in data[:50]]
    
    def _format_dota2_player(self, player_data: Dict) -> Dict:
        """Format Dota 2 player data"""
        return {
            'player_id': player_data.get('account_id'),
            'player_name': player_data.get('personaname'),
            'rank_tier': player_data.get('rank_tier'),
            'leaderboard_rank': player_data.get('leaderboard_rank'),
            'win_rate': player_data.get('win_rate'),
            'games_played': player_data.get('games'),
            'game': 'dota2'
        }
    
    # ===============================
    # FACEIT Integration (Multiple Games)
    # ===============================
    
    async def get_faceit_tournaments(self, game: str = 'csgo') -> List[Dict]:
        """Fetch FACEIT tournament data"""
        endpoint = f"/tournaments"
        params = {'game': game, 'type': 'upcoming', 'limit': 50}
        data = await self._make_request('faceit', endpoint, params)
        
        tournaments = []
        for tournament in data.get('items', []):
            tournaments.append({
                'tournament_id': tournament.get('tournament_id'),
                'name': tournament.get('name'),
                'game': tournament.get('game'),
                'region': tournament.get('region'),
                'prize_pool': tournament.get('prize_pool'),
                'max_teams': tournament.get('max_teams'),
                'teams_joined': tournament.get('teams_joined'),
                'started_at': tournament.get('started_at'),
                'finished_at': tournament.get('finished_at')
            })
        
        return tournaments
    
    async def get_faceit_player_stats(self, player_id: str, game: str = 'csgo') -> Dict:
        """Fetch FACEIT player statistics"""
        endpoint = f"/players/{player_id}/stats/{game}"
        data = await self._make_request('faceit', endpoint)
        
        stats = data.get('segments', [{}])[0].get('stats', {})
        return {
            'player_id': player_id,
            'game': game,
            'skill_level': stats.get('Skill Level', {}).get('value'),
            'elo': stats.get('Faceit Elo', {}).get('value'),
            'kd_ratio': stats.get('K/D Ratio', {}).get('value'),
            'win_rate': stats.get('Win Rate %', {}).get('value'),
            'average_kills': stats.get('Average Kills', {}).get('value'),
            'average_deaths': stats.get('Average Deaths', {}).get('value'),
            'headshot_percentage': stats.get('Headshot %', {}).get('value')
        }
    
    # ===============================
    # Unified Data Fetching
    # ===============================
    
    async def fetch_all_matches(self, games: List[str] = None) -> Dict[str, List[Dict]]:
        """Fetch matches from all supported games"""
        games = games or ['csgo', 'valorant', 'dota2']
        results = {}
        
        tasks = []
        if 'csgo' in games:
            tasks.append(('csgo', self.get_csgo_matches()))
        if 'valorant' in games:
            tasks.append(('valorant', self.get_valorant_matches()))
        if 'dota2' in games:
            tasks.append(('dota2', self.get_dota2_matches()))
        
        for game, task in tasks:
            try:
                results[game] = await task
            except Exception as e:
                logger.error(f"Failed to fetch {game} matches: {e}")
                results[game] = []
        
        return results
    
    async def fetch_all_player_stats(self, games: List[str] = None) -> Dict[str, List[Dict]]:
        """Fetch player stats from all supported games"""
        games = games or ['csgo', 'dota2', 'valorant']
        results = {}
        
        tasks = []
        if 'csgo' in games:
            tasks.append(('csgo', self.get_csgo_player_stats()))
        if 'dota2' in games:
            tasks.append(('dota2', self.get_dota2_player_stats()))
        if 'valorant' in games:
            tasks.append(('valorant', self.get_valorant_leaderboard()))
        
        for game, task in tasks:
            try:
                results[game] = await task
            except Exception as e:
                logger.error(f"Failed to fetch {game} player stats: {e}")
                results[game] = []
        
        return results


# ===============================
# Background Data Sync Service
# ===============================

class DataSyncService:
    """Background service to sync external API data with local database"""
    
    def __init__(self, api_client: ESportsAPIClient):
        self.api_client = api_client
        self.sync_interval = 300  # 5 minutes
        self.last_sync = None
    
    async def sync_all_data(self):
        """Perform complete data synchronization"""
        logger.info("Starting data synchronization...")
        
        async with self.api_client:
            # Fetch all matches and player stats
            matches_data = await self.api_client.fetch_all_matches()
            player_data = await self.api_client.fetch_all_player_stats()
            
            # TODO: Store in database
            # This would integrate with your existing SQLAlchemy models
            
            self.last_sync = datetime.now()
            logger.info(f"Data sync completed at {self.last_sync}")
            
            return {
                'matches': matches_data,
                'players': player_data,
                'sync_time': self.last_sync.isoformat()
            }
    
    async def should_sync(self) -> bool:
        """Check if data sync is needed"""
        if not self.last_sync:
            return True
        
        time_since_sync = datetime.now() - self.last_sync
        return time_since_sync.total_seconds() > self.sync_interval


# ===============================
# Usage Examples
# ===============================

async def example_usage():
    """Example of how to use the API client"""
    
    async with ESportsAPIClient() as client:
        # Fetch CS:GO matches
        csgo_matches = await client.get_csgo_matches(limit=10)
        print(f"Found {len(csgo_matches)} CS:GO matches")
        
        # Fetch Valorant leaderboard
        valorant_players = await client.get_valorant_leaderboard()
        print(f"Found {len(valorant_players)} Valorant players")
        
        # Fetch Dota 2 matches
        dota_matches = await client.get_dota2_matches(limit=10)
        print(f"Found {len(dota_matches)} Dota 2 matches")
        
        # Fetch all data at once
        all_matches = await client.fetch_all_matches()
        all_players = await client.fetch_all_player_stats()
        
        return {
            'matches': all_matches,
            'players': all_players
        }

if __name__ == "__main__":
    # Test the API client
    asyncio.run(example_usage())
