from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

def get_database_url():
    # Define the default database URL
    default_database_url = "sqlite:///./app.db"

    # You can customize the database URL based on environment variables or configuration settings
    # For example, you can use an environment variable to specify the test database URL
    test_database_url = "sqlite:///./test.db"

    # Use the default database URL by default
    database_url = default_database_url

    # Check if running tests and use the test database URL if so
    import sys
    if "pytest" in sys.modules:
        database_url = test_database_url

    return database_url

# Get the database URL
database_url = get_database_url()

# Create the SQLAlchemy engine
engine = create_engine(database_url)

# Create a sessionmaker object to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for all your SQLAlchemy models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, unique=True, index=True)
    last_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

