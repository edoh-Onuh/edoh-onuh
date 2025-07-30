#!/usr/bin/env python3
"""
Simple server startup script
"""
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting E-Sport Analytics Backend...")
    print("📍 Server: http://127.0.0.1:8001")
    print("📖 Docs: http://127.0.0.1:8001/docs")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8001,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")
