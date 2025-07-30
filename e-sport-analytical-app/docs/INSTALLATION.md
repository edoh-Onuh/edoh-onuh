# Installation Guide

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 14+** (for frontend)
- **MySQL 8.0+** (for database) or SQLite (for development)
- **npm** or **yarn** (package manager)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/e-sport-analytical-app.git
cd e-sport-analytical-app
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Database Configuration

**Option A: MySQL (Recommended for Production)**
1. Install MySQL 8.0+
2. Create database:
```sql
CREATE DATABASE esport_analytics;
CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON esport_analytics.* TO 'your_user'@'localhost';
```

3. Create `.env` file in backend directory:
```env
DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_NAME=esport_analytics
```

**Option B: SQLite (Quick Development Setup)**
The app will automatically use SQLite if MySQL connection fails.

#### Populate Sample Data
```bash
python populate_data.py
```

#### Start Backend Server
```bash
python run_server.py
```

The backend will be available at: http://127.0.0.1:8000

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Frontend Server
```bash
npm start
```

The frontend will be available at: http://localhost:3000

## Development Setup

### Using VS Code Tasks (Recommended)

If you're using VS Code, you can use the configured tasks:

1. **Start Backend**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Start Backend Server"
2. **Start Frontend**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Start Frontend"
3. **Start Both**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Start Full Application"

### Manual Setup

#### Backend (Terminal 1)
```bash
cd backend
python run_server.py
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm start
```

## Environment Variables

### Backend (.env file)
```env
# Database Configuration
DB_USER=your_mysql_user
DB_PASS=your_mysql_password
DB_HOST=localhost
DB_NAME=esport_analytics

# Optional: API Configuration
API_BASE_URL=http://127.0.0.1:8000
DEBUG=True
```

### Frontend (.env file - optional)
```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000/api/esport
```

## Troubleshooting

### Common Issues

#### Backend Issues

**1. Module 'app' not found**
- Ensure you're running the server from the `backend` directory
- Check that `app/__init__.py` exists

**2. Database connection failed**
- Verify MySQL is running
- Check database credentials in `.env` file
- The app will fallback to SQLite if MySQL fails

**3. Port 8000 already in use**
- Stop any existing backend processes
- Or change the port in `run_server.py`

#### Frontend Issues

**1. Port 3000 already in use**
- Choose a different port when prompted
- Or kill the existing process: `lsof -ti:3000 | xargs kill -9`

**2. API connection failed**
- Ensure backend is running on http://127.0.0.1:8000
- Check CORS settings if accessing from different domain

**3. Charts not displaying**
- Ensure sample data is populated: `python populate_data.py`
- Check browser console for JavaScript errors

### Database Issues

**Reset Database**
```bash
cd backend
python check_database.py  # Verify connection
python populate_data.py   # Repopulate data
```

**View Database Contents**
```bash
python quick_data.py  # Show sample data
```

## Performance Optimization

### Production Deployment

1. **Backend**: Use production ASGI server like Gunicorn
2. **Frontend**: Build optimized bundle with `npm run build`
3. **Database**: Use MySQL with proper indexing
4. **Caching**: Implement Redis for API caching
5. **Load Balancing**: Use Nginx for load balancing

### Development Tips

- Use the `--reload` flag for backend auto-restart
- Frontend has hot-reload enabled by default
- Check browser network tab for API response times
- Use React Developer Tools for component debugging
