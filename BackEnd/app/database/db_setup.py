from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from ..config import settings
import time, logging

MAX_RETRIES = 3
RETRY_INTERVAL = 5

SQLALCHEMY_DATABASE_URL = f"mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"init_command": "SET time_zone='+08:00'"}, 
    pool_pre_ping=True,
    pool_size=100, 
    max_overflow=50, 
    pool_timeout=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Generator function that attempts to establish a database connection.

    Yields:
        Session: A SQLAlchemy session object if the connection is successful.

    Raises:
        Exception: If the maximum number of retries is reached without a successful connection.
    """
    retries = 0
    while retries < MAX_RETRIES:
        """Create a new session instance."""
        db = SessionLocal()
        try:
            yield db    # Yield the database session back to the caller.
            return      # Exit the loop and yield the db if successful
        except SQLAlchemyError as e:
            if db is not None:
                db.rollback()   # Rollback the session to avoid any corrupted state.
                db.close()      # Close the session to release the connection.
            
            logging.error(
                f"SQLAlchemy error occurred: {str(e)}. "
                "Retrying in {RETRY_INTERVAL} seconds..."
            )
            time.sleep(RETRY_INTERVAL)
            retries += 1
        finally:
            db.close()
    else:
        logging.error(
            "Max retries reached. Unable to establish database connection."
        )
        raise Exception(
            "Max retries reached. Unable to establish database connection."
        )