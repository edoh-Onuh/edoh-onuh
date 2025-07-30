#!/usr/bin/env python3
"""
E-Sport Analytics Platform - API Setup Script
Helps users configure external API integrations
"""

import os
import sys
import shutil
from pathlib import Path
import requests
import time

class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

def setup_environment_file():
    """Setup .env file with API keys"""
    print_header("🔧 Setting Up Environment Configuration")
    
    backend_dir = Path(__file__).parent
    env_example = backend_dir / ".env.example"
    env_file = backend_dir / ".env"
    
    if not env_example.exists():
        print_error("❌ .env.example file not found!")
        return False
    
    if env_file.exists():
        overwrite = input(f"{Colors.WARNING}⚠️  .env file already exists. Overwrite? (y/N): {Colors.ENDC}")
        if overwrite.lower() != 'y':
            print_info("Keeping existing .env file")
            return True
    
    # Copy example file
    shutil.copy(env_example, env_file)
    print_success("Created .env file from template")
    
    # Get API keys from user
    print(f"\n{Colors.OKBLUE}🔑 Let's configure your API keys:")
    print("You can skip any API key and add it later to the .env file{Colors.ENDC}")
    
    api_keys = {}
    
    # Riot Games API
    print(f"\n{Colors.OKCYAN}🎮 Riot Games API (Valorant, League of Legends){Colors.ENDC}")
    print("Get your key from: https://developer.riotgames.com/")
    riot_key = input("Enter your Riot API key (or press Enter to skip): ").strip()
    if riot_key:
        api_keys['RIOT_API_KEY'] = riot_key
    
    # Steam API
    print(f"\n{Colors.OKCYAN}🎮 Steam Web API (CS:GO, Dota 2){Colors.ENDC}")
    print("Get your key from: https://steamcommunity.com/dev/apikey")
    steam_key = input("Enter your Steam API key (or press Enter to skip): ").strip()
    if steam_key:
        api_keys['STEAM_API_KEY'] = steam_key
    
    # FACEIT API
    print(f"\n{Colors.OKCYAN}🎮 FACEIT API (Multiple games, tournaments){Colors.ENDC}")
    print("Get your key from: https://developers.faceit.com/")
    faceit_key = input("Enter your FACEIT API key (or press Enter to skip): ").strip()
    if faceit_key:
        api_keys['FACEIT_API_KEY'] = faceit_key
    
    # Update .env file with provided keys
    if api_keys:
        with open(env_file, 'r') as f:
            content = f.read()
        
        for key, value in api_keys.items():
            content = content.replace(f"{key}=your-{key.lower().replace('_', '-')}-key-here", f"{key}={value}")
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print_success(f"Updated .env file with {len(api_keys)} API keys")
    
    return True

def test_api_connections():
    """Test connections to external APIs"""
    print_header("🧪 Testing API Connections")
    
    # Load environment variables
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print_error(".env file not found. Run setup first.")
        return
    
    # Read API keys
    api_keys = {}
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                api_keys[key] = value
    
    # Test free APIs first
    print(f"\n{Colors.OKBLUE}Testing free APIs (no key required):{Colors.ENDC}")
    
    # Test HLTV (CS:GO data)
    try:
        response = requests.get("https://hltv-api.vercel.app/api/matches", timeout=10)
        if response.status_code == 200:
            print_success("HLTV API (CS:GO) - Working")
        else:
            print_warning(f"HLTV API - Status {response.status_code}")
    except Exception as e:
        print_error(f"HLTV API - Failed: {e}")
    
    # Test OpenDota (Dota 2 data)
    try:
        response = requests.get("https://api.opendota.com/api/proMatches", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"OpenDota API (Dota 2) - Working ({len(data)} matches)")
        else:
            print_warning(f"OpenDota API - Status {response.status_code}")
    except Exception as e:
        print_error(f"OpenDota API - Failed: {e}")
    
    # Test APIs requiring keys
    print(f"\n{Colors.OKBLUE}Testing APIs with keys:{Colors.ENDC}")
    
    # Test Riot Games API
    if 'RIOT_API_KEY' in api_keys and api_keys['RIOT_API_KEY'] != 'your-riot-api-key-here':
        try:
            headers = {'X-Riot-Token': api_keys['RIOT_API_KEY']}
            response = requests.get(
                "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/test/123",
                headers=headers,
                timeout=10
            )
            if response.status_code in [200, 404]:  # 404 is expected for test account
                print_success("Riot Games API - Key is valid")
            else:
                print_warning(f"Riot Games API - Status {response.status_code}")
        except Exception as e:
            print_error(f"Riot Games API - Failed: {e}")
    else:
        print_warning("Riot Games API - No key configured")
    
    # Test Steam API
    if 'STEAM_API_KEY' in api_keys and api_keys['STEAM_API_KEY'] != 'your-steam-api-key-here':
        try:
            params = {'key': api_keys['STEAM_API_KEY'], 'format': 'json'}
            response = requests.get(
                "https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/",
                params=params,
                timeout=10
            )
            if response.status_code == 200:
                print_success("Steam Web API - Key is valid")
            else:
                print_warning(f"Steam Web API - Status {response.status_code}")
        except Exception as e:
            print_error(f"Steam Web API - Failed: {e}")
    else:
        print_warning("Steam Web API - No key configured")
    
    # Test FACEIT API
    if 'FACEIT_API_KEY' in api_keys and api_keys['FACEIT_API_KEY'] != 'your-faceit-api-key-here':
        try:
            headers = {'Authorization': f"Bearer {api_keys['FACEIT_API_KEY']}"}
            response = requests.get(
                "https://open-api.faceit.com/data/v4/games",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print_success(f"FACEIT API - Working ({len(data.get('items', []))} games)")
            else:
                print_warning(f"FACEIT API - Status {response.status_code}")
        except Exception as e:
            print_error(f"FACEIT API - Failed: {e}")
    else:
        print_warning("FACEIT API - No key configured")

def install_dependencies():
    """Install required Python packages"""
    print_header("📦 Installing Dependencies")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print_error("requirements.txt not found!")
        return False
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("All dependencies installed successfully")
            return True
        else:
            print_error(f"Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Error installing dependencies: {e}")
        return False

def check_database_connection():
    """Check database connection"""
    print_header("🗄️  Checking Database Connection")
    
    try:
        # Try to import SQLAlchemy and test connection
        from sqlalchemy import create_engine, text
        from app.database import get_database_url
        
        engine = create_engine(get_database_url())
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print_success("Database connection successful")
            return True
    except ImportError:
        print_warning("Database modules not available. Install dependencies first.")
        return False
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        print_info("Make sure MySQL is running and credentials are correct in .env")
        return False

def show_getting_started_guide():
    """Show getting started guide"""
    print_header("🚀 Getting Started Guide")
    
    print(f"""
{Colors.OKGREEN}Your E-Sport Analytics Platform is ready!{Colors.ENDC}

{Colors.OKCYAN}🔧 Available Data Sources:{Colors.ENDC}
• CS:GO: HLTV (free) + FACEIT (with API key)
• Valorant: Riot Games API (requires key)
• Dota 2: OpenDota (free) + Steam API (with key)

{Colors.OKCYAN}📡 Live Data Endpoints:{Colors.ENDC}
• GET /api/esport/live/matches/live - Real-time match data
• GET /api/esport/live/players/live - Live player statistics
• GET /api/esport/live/tournaments - Tournament information
• GET /api/esport/live/status - API status and health

{Colors.OKCYAN}🎮 Supported Games:{Colors.ENDC}
• csgo - Counter-Strike: Global Offensive
• valorant - Valorant
• dota2 - Dota 2

{Colors.OKCYAN}▶️  Next Steps:{Colors.ENDC}
1. Start the backend server: python run_server.py
2. Start the frontend: cd ../frontend && npm start
3. Visit the API docs: http://127.0.0.1:8000/docs
4. Open the dashboard: http://localhost:3000

{Colors.OKCYAN}💡 Pro Tips:{Colors.ENDC}
• Use the "Live Data" toggle in the dashboard to switch between sample and real data
• Configure more API keys in .env file for additional data sources
• Check /api/esport/live/status for API health and cache status
• Use force_refresh=true parameter to bypass cache and get fresh data

{Colors.WARNING}⚠️  API Rate Limits:{Colors.ENDC}
• HLTV: 100 requests/minute (free)
• OpenDota: 60 requests/minute (free)
• Riot Games: 100 requests/2 minutes (with key)
• FACEIT: 1000 requests/minute (with key)

Enjoy your real-world e-sports analytics! 🎮📊
    """)

def main():
    """Main setup function"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║               🎮 E-Sport Analytics Platform                   ║
║                    API Setup & Configuration                 ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")
    
    print("This script will help you set up real-world e-sports API integrations.")
    print("You'll be able to fetch live data from CS:GO, Valorant, and Dota 2!")
    
    # Setup steps
    steps = [
        ("📝 Setup environment file", setup_environment_file),
        ("📦 Install dependencies", install_dependencies),
        ("🧪 Test API connections", test_api_connections),
        ("🗄️  Check database", check_database_connection),
        ("📖 Show guide", show_getting_started_guide)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{Colors.OKCYAN}{'='*60}")
        print(f"  {step_name}")
        print(f"{'='*60}{Colors.ENDC}")
        
        try:
            if callable(step_func):
                result = step_func()
                if result is False:
                    print_warning(f"Step '{step_name}' had issues but continuing...")
            time.sleep(1)  # Brief pause between steps
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Setup interrupted by user.{Colors.ENDC}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error in step '{step_name}': {e}")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Setup completed! Your platform is ready for real-world e-sports data!{Colors.ENDC}")

if __name__ == "__main__":
    main()
