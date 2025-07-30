#!/usr/bin/env python3
"""
CSV Data Importer for E-Sport Analytics App
Imports data from CSV files into the database
"""

import pandas as pd
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models import Match, PlayerStat, PositionFrequency, Base

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

def import_matches_from_csv(csv_file="data/matches_sample.csv"):
    """Import matches from CSV file"""
    try:
        print(f"📁 Importing matches from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        matches = []
        for _, row in df.iterrows():
            match = Match(
                team_name=row['team_name'],
                opponent_name=row['opponent_name'],
                result=row['result'],
                match_date=datetime.strptime(row['match_date'], '%Y-%m-%d'),
                score_team=int(row['score_team']),
                score_opponent=int(row['score_opponent']),
                game_mode=row['game_mode']
            )
            matches.append(match)
        
        session.add_all(matches)
        session.commit()
        print(f"✅ Imported {len(matches)} matches")
        return matches
        
    except Exception as e:
        print(f"❌ Error importing matches: {e}")
        session.rollback()
        return []

def import_player_stats_from_csv(csv_file="data/player_stats_sample.csv"):
    """Import player stats from CSV file"""
    try:
        print(f"📁 Importing player stats from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        stats = []
        for _, row in df.iterrows():
            stat = PlayerStat(
                player_name=row['player_name'],
                kills=int(row['kills']),
                deaths=int(row['deaths']),
                assists=int(row['assists']),
                match_id=int(row['match_id']),
                kda_ratio=float(row['kda_ratio'])
            )
            stats.append(stat)
        
        session.add_all(stats)
        session.commit()
        print(f"✅ Imported {len(stats)} player stat records")
        return stats
        
    except Exception as e:
        print(f"❌ Error importing player stats: {e}")
        session.rollback()
        return []

def import_positions_from_csv(csv_file="data/position_frequency_sample.csv"):
    """Import position data from CSV file"""
    try:
        print(f"📁 Importing position data from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        positions = []
        for _, row in df.iterrows():
            position = PositionFrequency(
                x=float(row['x']),
                y=float(row['y']),
                frequency=int(row['frequency']),
                player_name=row['player_name'],
                map_name=row['map_name']
            )
            positions.append(position)
        
        session.add_all(positions)
        session.commit()
        print(f"✅ Imported {len(positions)} position records")
        return positions
        
    except Exception as e:
        print(f"❌ Error importing positions: {e}")
        session.rollback()
        return []

def main():
    """Main function to import all CSV data"""
    print("📊 E-Sport Analytics CSV Data Importer")
    print("=" * 50)
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
        
        # Import data from CSV files
        matches = import_matches_from_csv()
        player_stats = import_player_stats_from_csv()
        positions = import_positions_from_csv()
        
        # Summary
        print(f"\n🎉 Import Complete!")
        print(f"📈 Total imported:")
        print(f"   🎮 Matches: {len(matches)}")
        print(f"   📊 Player Stats: {len(player_stats)}")
        print(f"   🗺️ Positions: {len(positions)}")
        
        print(f"\n📍 You can now view your data at:")
        print(f"   🌐 Frontend: http://localhost:3000")
        print(f"   📖 API Docs: http://127.0.0.1:8000/docs")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
