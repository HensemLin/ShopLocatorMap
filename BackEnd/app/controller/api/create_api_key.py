import datetime, pytz
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException, Depends
from ...database.db_setup import get_db
from ...database import db_models
from ... import schemas
from ...utils import utils
import logging


async def create_api_key(db: Session = Depends(get_db)):
    """
    Create a new API key for the company.

    Args:
        db (Session): The database session.

    Raises:
        HTTPException: If any unexpected error occurs.
    """
    try:      
        """Generate a new API key and its ID"""
        api_key = utils.generate_api_key()
        api_key_id = utils.generate_unique_id()

        """Add the new API key object to the database"""
        new_hashed_api_key = db_models.ApiKey(
            apiKey_id=api_key_id,
            apiKey=utils.hash(api_key)
        )

        db.add(new_hashed_api_key)

        """Commit the changes to the database"""
        db.commit()

        return schemas.ApiKeyOut(
            id=api_key_id,
            apiKey=api_key,
            created_at=datetime.datetime.now(
                pytz.timezone('Asia/Kuala_Lumpur')
            ).strftime("%Y-%m-%dT%H:%M:%S")
        )
    
    except SQLAlchemyError as sqla_error:
        logging.error("SQLAlchemy error occurred: {}".format(str(sqla_error)))
        db.rollback()  # Rollback the transaction in case of an SQLAlchemy error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )