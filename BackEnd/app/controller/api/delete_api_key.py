from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException, Depends
from ...database.db_setup import get_db
from ...database import db_models
import logging

async def delete_api_key(
        id: str, 
        db: Session = Depends(get_db)
    ):
    """
    Deletes a specific API key by ID.

    Args:
        id (str): The ID of the API key to delete.
        db (Session): The database session dependency.

    Returns:
        Response: A response indicating the successful deletion of the API key.

    Raises:
        HTTPException: If any error happened in the sqlalchemy
        HTTPException: If the API key with the specified ID does not exist, a 404 Not Found error is raised.
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try:
        """Query the API key by ID"""
        api_key_query = db.query(
            db_models.ApiKey
        ).filter(
            db_models.ApiKey.apiKey_id == id,
        )
        
        api_key = api_key_query.first()

        """If the API key does not exist, raise a 404 Not Found error"""
        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"API key with ID: {id} does not exist"
            )

        """Delete the API key and commit the transaction"""
        api_key_query.delete(synchronize_session=False)
        db.commit()
    
    except HTTPException as http_exception:
        raise http_exception
    
    except SQLAlchemyError as sqla_error:
        logging.error("SQLAlchemy error occurred: {}".format(str(sqla_error)))
        db.rollback()  # Rollback the transaction in case of an SQLAlchemy error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
