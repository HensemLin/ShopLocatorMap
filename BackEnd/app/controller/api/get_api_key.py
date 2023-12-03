from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException, Depends
from ...database.db_setup import get_db
from ...database import db_models
import logging

async def get_api_key( db: Session = Depends(get_db)):
    """
    Get all API keys for the given company.

    Args:
        db (Session): The database session.

    Raises:
        HTTPException: If no API keys are found for the company 
                        or if any unexpected error occurs.
    """
    try:    
        """Get all API keys for the given company from the database"""
        api_keys = db.query(
            db_models.ApiKey
        ).all()

        """If no API keys are found, raise a 404 Not Found error"""
        if not api_keys:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No API key(s) found"
            )

        """Set the 'id' attribute of each API key to 'apiKey_id'"""
        for api_key in api_keys:
            api_key.id = api_key.apiKey_id
        
        return api_keys
    
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
    
async def get_api_key_by_id(
        id: str, 
        db: Session = Depends(get_db)
    ):
    """
    Get a specific API key for the given company.

    Args:
        id (str): The ID of the API key to retrieve.
        db (Session): The database session.

    Raises:
        HTTPException: If the specified API key is not found, a 404 Not Found Error is raised.  
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try:
        api_key = db.query(
            db_models.ApiKey
        ).filter(
            db_models.ApiKey.apiKey_id == id,
        ).first()
        
        """If the API key is not found, raise a 404 Not Found error"""
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No API key(s) found"
            )

        """Set the 'id' attribute of the API key to 'apiKey_id'"""
        api_key.id = api_key.apiKey_id

        return api_key
    
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