#!/usr/bin/env python3
"""
Quick Data Generator - Creates minimal sample data for testing
"""

import requests
import json
from datetime import datetime, timedelta
import random

# API base URL (adjust if needed)
API_BASE = "http://127.0.0.1:8000/api/esport"

def create_sample_matches():
    """Create sample matches via API"""
    teams = ["Team Liquid", "Cloud9", "TSM", "G2 Esports", "Fnatic"]
    
    matches_data = []
    for i in range(10):
        team = random.choice(teams)
        opponent = random.choice([t for t in teams if t != team])
        team_score = random.randint(10, 16)
        opponent_score = random.randint(8, 15)
        
        match_data = {
            "team_name": team,
            "opponent_name": opponent,
            "result": "win" if team_score > opponent_score else "loss",
            "score_team": team_score,
            "score_opponent": opponent_score,
            "game_mode": "Competitive"
        }
        matches_data.append(match_data)
    
    return matches_data

def create_sample_player_stats():
    """Create sample player statistics"""
    players = ["s1mple", "ZywOo", "device", "NiKo", "electronic"]
    
    stats_data = []
    for player in players:
        for i in range(3):  # 3 records per player
            kills = random.randint(15, 30)
            deaths = random.randint(8, 20)
            assists = random.randint(5, 15)
            
            stat_data = {
                "player_name": player,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "match_id": i + 1,
                "kda_ratio": round((kills + assists) / max(deaths, 1), 2)
            }
            stats_data.append(stat_data)
    
    return stats_data

def print_sample_data():
    """Print sample data that can be manually inserted"""
    print("🎮 SAMPLE MATCHES DATA:")
    print("=" * 50)
    matches = create_sample_matches()
    for i, match in enumerate(matches[:5], 1):
        print(f"{i}. {match['team_name']} vs {match['opponent_name']}: {match['score_team']}-{match['score_opponent']} ({match['result']})")
    
    print("\n📊 SAMPLE PLAYER STATS:")
    print("=" * 50)
    stats = create_sample_player_stats()
    for i, stat in enumerate(stats[:10], 1):
        print(f"{i}. {stat['player_name']}: {stat['kills']}K/{stat['deaths']}D/{stat['assists']}A (KDA: {stat['kda_ratio']})")
    
    print("\n🗺️ SAMPLE POSITION DATA:")
    print("=" * 50)
    for i in range(5):
        x, y = random.randint(100, 900), random.randint(100, 900)
        freq = random.randint(1, 10)
        print(f"{i+1}. Position ({x}, {y}) - Frequency: {freq}")

if __name__ == "__main__":
    print_sample_data()
