#!/usr/bin/env python3
"""
Database Table Inspector - Check current table structure
"""

from sqlalchemy import text, inspect
from app.database import engine
from app.models import Base

def check_table_structure():
    """Check the current structure of database tables"""
    try:
        inspector = inspect(engine)
        
        print("🔍 Current Database Tables:")
        print("=" * 50)
        
        tables = inspector.get_table_names()
        print(f"Available tables: {tables}")
        
        for table_name in tables:
            print(f"\n📋 Table: {table_name}")
            columns = inspector.get_columns(table_name)
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
        
        return tables
        
    except Exception as e:
        print(f"❌ Error inspecting database: {e}")
        return []

def recreate_tables():
    """Drop and recreate all tables with correct structure"""
    try:
        print("\n🔄 Recreating tables with correct structure...")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✅ Dropped existing tables")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Created tables with correct structure")
        
        return True
        
    except Exception as e:
        print(f"❌ Error recreating tables: {e}")
        return False

def main():
    print("🔧 Database Table Structure Checker")
    print("=" * 50)
    
    # Check current structure
    tables = check_table_structure()
    
    if tables:
        response = input("\nRecreate tables with correct structure? (y/N): ").lower().strip()
        if response in ['y', 'yes']:
            if recreate_tables():
                print("\n✅ Tables recreated successfully!")
                check_table_structure()
            else:
                print("\n❌ Failed to recreate tables")
    else:
        print("No tables found, creating new ones...")
        recreate_tables()

if __name__ == "__main__":
    main()
