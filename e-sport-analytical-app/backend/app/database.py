#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from azure.identity import DefaultAzureCredential
#from azure.keyvault.secrets import SecretClient

# Azure Key Vault setup
#VAULT_URL = "https://adanu-e-sport.vault.azure.net/"  
#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=VAULT_URL, credential=credential)

# Retrieve secrets from Key Vault
#db_user = client.get_secret("db-user").value
#db_pass = client.get_secret("db-password").value
#db_host = client.get_secret("db-host").value
#db_name = client.get_secret("db-name").value

# Build MySQL connection URL
#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

# Set up SQLAlchemy engine and sessionmaker
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

print("--- Attempting to load database configuration ---")

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# --- DEBUGGING PRINTS ---
# These lines will show us if the .env file is being read correctly.
print(f"DB_USER: {db_user}")
print(f"DB_PASS: {db_pass}")
print(f"DB_HOST: {db_host}")
print(f"DB_NAME: {db_name}")
# --- END DEBUGGING PRINTS ---

# Check if any variable is None, which would cause an error
if not all([db_user, db_pass, db_host, db_name]):
    print("\n[ERROR] One or more environment variables are not set.")
    print("Please ensure the .env file is in the 'backend' directory and is correct.\n")
    # We exit here to prevent the crash
    exit()

# Build MySQL connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

print(f"Connecting to database at: {SQLALCHEMY_DATABASE_URL}")
print("-------------------------------------------------")

# Set up SQLAlchemy engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """
    Dependency that provides a database session.
    Used by FastAPI endpoints to access the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_database_url():
    """
    Returns the database URL for external use
    """
    return SQLALCHEMY_DATABASE_URL


if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection error:", e)
