#!/usr/bin/env python3
"""
Simple backend server starter
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting E-Sport Analytics Backend Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📖 API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
