# 🎮 E-Sport Analytics Platform

> A comprehensive e-sport analytics platform built with React frontend and FastAPI backend, featuring real-time player statistics, match predictions, and interactive visualizations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479a1.svg)](https://www.mysql.com/)

![Dashboard Preview](docs/dashboard-preview.png)

## ✨ Features

### 🌐 **Real-World Data Integration** ✨ NEW!
- **Live API Support** - Real-time data from CS:GO, Valorant, and Dota 2
- **Multiple Data Sources** - HLTV, OpenDota, Riot Games, FACEIT, Steam APIs
- **Smart Data Toggle** - Switch between sample data and live data seamlessly
- **Auto-Sync Background Service** - Automatic data updates every 5 minutes
- **Rate Limit Management** - Intelligent caching and request optimization

### 📊 **Advanced Analytics Dashboard**
- **Real-time Player Statistics** - K/D/A ratios, efficiency metrics, and performance tracking
- **Match Analysis** - Comprehensive match history with win/loss trends
- **Interactive Visualizations** - Area charts, bar charts, pie charts, and scatter plots
- **Position Heatmaps** - Player positioning frequency analysis
- **Quick Stats Overview** - Total matches, win rates, player counts, and average KDA
- **Tournament Data** - Live tournament schedules and results

### 🔍 **Smart Search System**
- **Dual Search Mode** - Toggle between team and player searches
- **Dynamic Filtering** - Real-time results with smart suggestions
- **Performance Metrics** - Instant statistics calculation and display
- **Reset Functionality** - Quick reset for new searches
- **Multi-Game Support** - Search across CS:GO, Valorant, and Dota 2

### 🎯 **Predictive Analytics**
- **Match Outcome Predictions** - AI-powered win probability calculations
- **Team Performance Analysis** - Historical data-driven insights
- **Trending Analytics** - Real-time insights and performance trends
- **Player Efficiency Metrics** - Advanced performance scoring

### 🎨 **Modern UI/UX**
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Smooth Animations** - Framer Motion powered interactions
- **Dark Mode Support** - Elegant light/dark theme switching
- **Gradient Aesthetics** - Modern glass-morphism design language

## 🏗️ Architecture

```mermaid
graph LR
    A[React Frontend :3000] <--> B[FastAPI Backend :8000]
    B <--> C[MySQL Database]
    B <--> D[SQLite Fallback]
    A --> E[Recharts Visualizations]
    A --> F[Tailwind CSS Styling]
    A --> G[Framer Motion Animations]
```

### 🛠️ Tech Stack

#### Frontend
- **React 18.3.1** - Modern React with hooks and functional components
- **Recharts** - Professional chart library for data visualization
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and interactions
- **Axios** - HTTP client for API communication
- **Clsx & Tailwind-merge** - Conditional styling utilities

#### Backend
- **FastAPI** - High-performance async Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **MySQL/SQLite** - Primary and fallback database systems
- **Python 3.8+** - Modern Python with async/await support

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.8+
- **MySQL** 8.0+ (Database)
- **Git** for version control

### 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/esport-analytics.git
   cd esport-analytics
   ```

2. **Automated Setup (Recommended)**
   ```bash
   # Windows
   setup.bat
   
   # This script will:
   # - Set up Python virtual environment
   # - Install backend dependencies
   # - Install frontend dependencies
   # - Create environment configuration
   ```

3. **Manual Setup**
   
   **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```
   
   **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Database Configuration**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Edit .env with your MySQL credentials:
   # DATABASE_URL=mysql://username:password@localhost/esport_analytics
   # API_KEY_STEAM=your_steam_api_key
   # API_KEY_RIOT=your_riot_api_key
   ```

5. **Initialize Database**
   ```bash
   cd backend
   python populate_database_now.py
   # This will create and populate the database with sample data
   ```

## 📖 Documentation

- **[Live Data Integration Guide](docs/LIVE_DATA_INTEGRATION.md)** - Set up real-world APIs ✨
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute
- **[License](LICENSE)** - MIT License details

## 🎯 Usage Examples

### Search for Team Performance
1. Select "Team Search" mode
2. Enter team name (e.g., "TSM", "Astralis")
3. View comprehensive match analytics and player statistics

### Analyze Player Performance
1. Switch to "Player Search" mode
2. Enter player name (e.g., "device", "s1mple")
3. Explore KDA ratios, efficiency metrics, and performance trends

### Interactive Visualizations
- **Hover** over chart elements for detailed tooltips
- **Click** legend items to toggle data series
- **Resize** browser to see responsive chart adaptations

## 📊 Sample Data

The application includes rich sample data featuring:
- **50+ Professional Matches** from top e-sport teams
- **400+ Player Statistics** with realistic K/D/A ratios
- **300+ Position Records** for heatmap analysis
- **Popular Teams**: TSM, Astralis, NaVi, G2, FaZe, Liquid, NAVI, SK
- **Pro Players**: device, s1mple, ZywOo, NiKo, coldzera, and more

## 🔧 Development

### Project Structure
```
e-sport-analytical-app/
├── backend/                 # FastAPI backend
│   ├── app/                # Application modules
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   ├── models.py       # Database models
│   │   └── schemas.py      # Pydantic schemas
│   ├── data/               # Sample data files
│   ├── run_server.py       # Server startup script
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API service layer
│   │   └── App.js          # Main application
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
└── .vscode/                # VS Code configuration
```

### Available Scripts

#### Backend
```bash
python run_server.py        # Start development server
python populate_data.py     # Generate sample data
python check_database.py    # Verify database connection
python test_api.py          # Test API endpoints
```

#### Frontend
```bash
npm start                   # Start development server
npm run build              # Build for production
npm test                   # Run test suite
npm run eject              # Eject from Create React App
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Backend won't start?**
- Check Python version (3.8+ required)
- Verify you're in the `backend` directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Frontend shows no data?**
- Verify backend is running on http://127.0.0.1:8000
- Check browser console for API errors
- Ensure sample data is populated: `python populate_data.py`

**Database connection issues?**
- Check MySQL service status
- Verify credentials in `.env` file
- App will fallback to SQLite automatically

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Recharts** - Amazing React charting library
- **FastAPI** - Lightning-fast Python web framework
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Delightful React animations
- **VS Code** - Excellent development environment

## 📧 Contact

- **Developer**: John Edoh Onuh
- **Project Repository**: [GitHub](https://github.com/JohnEdohOnuh/e-sport-analytical-app)
- **Documentation**: [Docs](docs/)
- **Issues**: [GitHub Issues](https://github.com/JohnEdohOnuh/e-sport-analytical-app/issues)
- **Email**: adanu1947@gmail.com

---

<div align="center">
  <strong>🎮 Built with ❤️ for the E-Sport Community 🎮</strong>
</div>
- Tailwind CSS for styling
- Framer Motion for animations
- Recharts for data visualization

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- Pydantic for data validation
- Uvicorn ASGI server
- MySQL database

**Database:**
- MySQL 8.0
- Tables: matches, player_stats, position_frequency

##  Prerequisites

Before running this application, make sure you have:

- **Python 3.13+** installed
- **Node.js 16+** and npm
- **MySQL 8.0+** server running
- **Git** for version control

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/e-sport-analytical-app.git
cd e-sport-analytical-app
```

### 2. Database Setup
1. Start your MySQL server
2. Create a database named `esport_analytics`:
```sql
CREATE DATABASE esport_analytics;
```

3. Update database credentials in `backend/.env`:
```env
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_NAME=esport_analytics
```

### 3. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install fastapi uvicorn SQLAlchemy python-dotenv PyMySQL

# Start the backend server
python run_server.py
```

The backend will be available at `http://127.0.0.1:8000`

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
### 🎯 Running the Application

**Automated Launch (Windows)**
```bash
# From project root
.\launch_app.bat
```
This script will start both backend and frontend automatically.

**Manual Launch**
```bash
# Terminal 1 - Backend
cd backend
python run_server.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

**Access the application:**
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

##  API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/api/esport/matches/` | GET | Retrieve match data |
| `/api/esport/player-stats/` | GET | Get player statistics |
| `/api/esport/predict/` | GET | Match outcome predictions |
| `/api/esport/position-heatmap/` | GET | Position frequency data |

### Example API Calls

```bash
# Get all matches
curl http://127.0.0.1:8000/api/esport/matches/

# Get player statistics
curl http://127.0.0.1:8000/api/esport/player-stats/

# Get prediction for a team
curl "http://127.0.0.1:8000/api/esport/predict/?team=TeamA"

# Get heatmap data
curl http://127.0.0.1:8000/api/esport/position-heatmap/
```

##  📁 Project Structure

```
e-sport-analytical-app/
├── 📂 backend/                    # FastAPI Backend
│   ├── 📂 app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI application entry
│   │   ├── database.py           # Database configuration
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── 📂 routers/           # API route handlers
│   │   │   ├── matches.py        # Match data endpoints
│   │   │   ├── player_stats.py   # Player statistics
│   │   │   ├── predict.py        # ML predictions
│   │   │   ├── heatmap.py        # Position heatmaps
│   │   │   └── live_data.py      # Real-time data
│   │   └── 📂 services/          # Business logic
│   │       ├── external_apis.py  # API integrations
│   │       ├── matches.py        # Match services
│   │       └── player_stats.py   # Player services
│   ├── 📂 data/                  # Sample CSV data
│   ├── .env.example              # Environment template
│   ├── requirements.txt          # Python dependencies
│   ├── run_server.py             # Server startup
│   └── populate_database_now.py  # Database setup
├── 📂 frontend/                   # React Frontend
│   ├── 📂 public/                # Static assets
│   ├── 📂 src/
│   │   ├── 📂 components/        # React components
│   │   │   ├── LiveDataToggle.jsx # Live data switch
│   │   │   └── 📂 ui/            # UI components
│   │   ├── 📂 services/          # API service layer
│   │   │   └── api.js            # Backend API calls
│   │   ├── App.js               # Main application
│   │   ├── EsportDashboard.jsx  # Dashboard component
│   │   └── index.js             # React entry point
│   ├── package.json             # Node.js dependencies
│   └── ...
├── 📂 docs/                      # Documentation
│   ├── API.md                   # API documentation
│   ├── INSTALLATION.md          # Setup guide
│   └── LIVE_DATA_INTEGRATION.md # API integration guide
├── 📄 launch_app.bat            # Quick launcher (Windows)
├── 📄 setup.bat                 # Setup script (Windows)
├── 📄 README.md                 # This file
├── 📄 .gitignore               # Git ignore rules
└── 📄 LICENSE                   # MIT License
```

##  Development

### Backend Development
```bash
cd backend
# Start with auto-reload for development
python run_server.py
```

### Frontend Development
```bash
cd frontend
# Start development server with hot reload
npm start
```

### Database Schema
The application automatically creates the following tables:
- `matches` - Store match results and metadata
- `player_stats` - Track player performance metrics
- `position_frequency` - Log player position data for heatmaps

##  Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

##  Production Build

### Frontend Production Build
```bash
cd frontend
npm run build
```

### Backend Production Deployment
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

##  Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DB_USER=your_mysql_username
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_NAME=esport_analytics

# Optional: Azure Key Vault (for production)
# VAULT_URL=https://your-vault.vault.azure.net/
```

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'app'"**
   - Make sure you're running the backend from the `backend/` directory
   - Solution: `cd backend` then `python run_server.py`

2. **Database Connection Error**
   - Verify MySQL server is running
   - Check credentials in `.env` file
   - Ensure database `esport_analytics` exists

3. **Frontend Can't Connect to Backend**
   - Verify backend is running on port 8000
   - Check CORS configuration in `backend/app/main.py`
   - Ensure API base URL is correct in `frontend/src/services/api.js`

4. **Port Already in Use**
   - Backend: Change port in `run_server.py`
   - Frontend: Set `PORT=3001` environment variable

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request



##  Authors

- **John Edoh Onuh** - *Developer & Creator* - [GitHub Profile](https://github.com/JohnEdohOnuh)

## Acknowledgments

- FastAPI team for the excellent web framework
- React team for the frontend library
- MySQL for reliable data storage
- All contributors who helped with this project

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/e-sport-analytical-app/issues) page
2. Create a new issue with detailed description
3. Contact: adanu1947@gmail.com

---

⭐ **Star this repository if you found it helpful!**
