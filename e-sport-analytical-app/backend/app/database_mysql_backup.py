# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("--- Using SQLite for development (MySQL not available) ---")

# Create SQLite database in the backend directory
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "esport_analytics.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

print(f"Using SQLite database at: {DATABASE_PATH}")
print("--------------------------------------------------------")

# Set up SQLAlchemy engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection error:", e)
