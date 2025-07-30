#!/usr/bin/env python3
"""
E-Sport Analytics Data Population Script
Creates realistic sample data for matches, player stats, and position heatmaps
"""

import random
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from app.database import engine
from app.models import Match, PlayerStat, PositionFrequency, Base

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data configurations
TEAMS = [
    "Team Liquid", "Cloud9", "TSM", "G2 Esports", "Fnatic", 
    "NaVi", "Astralis", "FaZe Clan", "SK Gaming", "Virtus.pro",
    "NRG", "100 Thieves", "Evil Geniuses", "OG", "Alliance"
]

PLAYERS = [
    "s1mple", "ZywOo", "device", "NiKo", "coldzera", "FalleN", 
    "electronic", "Twistzz", "ropz", "sh1ro", "Ax1Le", "Hobbit",
    "rain", "olofmeister", "GuardiaN", "fer", "TACO", "Stewie2K",
    "autimatic", "RUSH", "tarik", "Skadoodle", "n0thing", "shroud",
    "pashaBiceps", "NEO", "TaZ", "Snax", "byali", "MICHU"
]

GAME_MODES = ["Competitive", "Ranked", "Tournament", "Scrim", "Practice"]

MAPS = ["Dust2", "Mirage", "Inferno", "Cache", "Overpass", "Train", "Cobblestone"]

def create_sample_matches(num_matches=50):
    """Create sample match data"""
    print(f"🎮 Creating {num_matches} sample matches...")
    
    matches = []
    for i in range(num_matches):
        team = random.choice(TEAMS)
        opponent = random.choice([t for t in TEAMS if t != team])
        
        # Random match outcome
        team_score = random.randint(0, 16)
        opponent_score = random.randint(0, 16)
        
        # Ensure one team wins (unless it's a draw in rare cases)
        if team_score == opponent_score:
            if random.random() > 0.1:  # 90% chance to avoid draw
                if random.random() > 0.5:
                    team_score += random.randint(1, 3)
                else:
                    opponent_score += random.randint(1, 3)
        
        result = "win" if team_score > opponent_score else ("loss" if team_score < opponent_score else "draw")
        
        # Random date within last 6 months
        days_ago = random.randint(1, 180)
        match_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        
        match = Match(
            team_name=team,
            opponent_name=opponent,
            result=result,
            match_date=match_date,
            score_team=team_score,
            score_opponent=opponent_score,
            game_mode=random.choice(GAME_MODES)
        )
        matches.append(match)
    
    session.add_all(matches)
    session.commit()
    print(f"✅ Created {len(matches)} matches")
    return matches

def create_sample_player_stats(matches, players_per_match=5):
    """Create sample player statistics for matches"""
    print(f"📊 Creating player statistics...")
    
    player_stats = []
    for match in matches:
        # Create stats for random players in this match
        match_players = random.sample(PLAYERS, min(players_per_match, len(PLAYERS)))
        
        for player in match_players:
            # Generate realistic K/D/A stats
            kills = random.randint(5, 30)
            deaths = random.randint(3, 25)
            assists = random.randint(2, 20)
            
            # Calculate KDA ratio
            kda_ratio = (kills + assists) / max(deaths, 1)
            
            stat = PlayerStat(
                player_name=player,
                kills=kills,
                deaths=deaths,
                assists=assists,
                match_id=match.id,
                kda_ratio=round(kda_ratio, 2),
                created_at=match.match_date
            )
            player_stats.append(stat)
    
    session.add_all(player_stats)
    session.commit()
    print(f"✅ Created {len(player_stats)} player stat records")
    return player_stats

def create_sample_position_data(num_positions=200):
    """Create sample position frequency data for heatmaps"""
    print(f"🗺️ Creating {num_positions} position data points...")
    
    positions = []
    for i in range(num_positions):
        # Create realistic map coordinates (assuming 1000x1000 map)
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        frequency = random.randint(1, 15)
        
        position = PositionFrequency(
            x=round(x, 2),
            y=round(y, 2),
            frequency=frequency,
            player_name=random.choice(PLAYERS),
            map_name=random.choice(MAPS),
            created_at=datetime.datetime.now() - datetime.timedelta(
                days=random.randint(1, 30)
            )
        )
        positions.append(position)
    
    session.add_all(positions)
    session.commit()
    print(f"✅ Created {len(positions)} position records")
    return positions

def clear_existing_data():
    """Clear existing data from tables"""
    print("🧹 Clearing existing data...")
    session.query(PositionFrequency).delete()
    session.query(PlayerStat).delete()
    session.query(Match).delete()
    session.commit()
    print("✅ Existing data cleared")

def display_data_summary():
    """Display summary of created data"""
    print("\n📈 DATA SUMMARY:")
    print("=" * 50)
    
    # Match summary
    total_matches = session.query(Match).count()
    wins = session.query(Match).filter(Match.result == 'win').count()
    losses = session.query(Match).filter(Match.result == 'loss').count()
    draws = session.query(Match).filter(Match.result == 'draw').count()
    
    print(f"🎮 Matches: {total_matches} total")
    print(f"   └─ Wins: {wins}, Losses: {losses}, Draws: {draws}")
    
    # Player stats summary
    total_stats = session.query(PlayerStat).count()
    avg_kills = session.query(PlayerStat).with_entities(
        func.avg(PlayerStat.kills).label('avg_kills')
    ).scalar()
    
    print(f"📊 Player Stats: {total_stats} records")
    print(f"   └─ Average Kills: {avg_kills:.1f}")
    
    # Position data summary
    total_positions = session.query(PositionFrequency).count()
    unique_players = session.query(PositionFrequency.player_name).distinct().count()
    
    print(f"🗺️ Position Data: {total_positions} points")
    print(f"   └─ Unique Players: {unique_players}")
    
    # Top 5 players by KDA
    top_players = session.query(PlayerStat).order_by(
        PlayerStat.kda_ratio.desc()
    ).limit(5).all()
    
    print(f"\n🏆 TOP 5 PLAYERS BY KDA:")
    for i, player in enumerate(top_players, 1):
        print(f"   {i}. {player.player_name}: {player.kda_ratio} KDA ({player.kills}K/{player.deaths}D/{player.assists}A)")

def main():
    """Main function to populate database with sample data"""
    print("🚀 E-Sport Analytics Data Population")
    print("=" * 50)
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        
        # Ask user if they want to clear existing data
        response = input("Clear existing data? (y/N): ").lower().strip()
        if response in ['y', 'yes']:
            clear_existing_data()
        
        # Create sample data
        matches = create_sample_matches(50)
        player_stats = create_sample_player_stats(matches, 8)
        positions = create_sample_position_data(300)
        
        # Display summary
        display_data_summary()
        
        print(f"\n🎉 Success! Your e-sport analytics app now has sample data!")
        print(f"📍 Backend API: http://127.0.0.1:8000/docs")
        print(f"🌐 Frontend App: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
