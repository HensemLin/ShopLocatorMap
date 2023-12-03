import sys, logging
from fastapi import status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from ..utils.location_scraper import LocationScraper
from . import db_models
from .db_setup import SessionLocal

def initialize_table_data():
    """
    Initialize data in the 'Company' and 'Source' tables.

    This function adds data to the 'Company' and 'Source' tables if it does not already exist.

    Returns:
        None
    """

    try:
        """Create a new database session"""
        db = SessionLocal()

        """Initialize data for the 'Shop' and 'ShopLocation' table"""
        print("Initializing....")
        shop_details = LocationScraper(url="https://zuscoffee.com/category/store/melaka/").shop_details
        for shop in shop_details:
            """Check if the company already exists in the database"""
            existing_shop = db.query(
                db_models.Shop
            ).filter(
                db_models.Shop.name==shop["shop"]
            ).all()

            """If the company does not exist, add it to the 'Company' table"""
            if not existing_shop:
                new_shop = db_models.Shop(
                    name = shop["shop"],
                    address = shop["address"]
                )
                db.add(new_shop)
                db.flush()

                new_shop_loc = db_models.ShopLocation(
                    shopId = new_shop.id,
                    lon = shop["location"]["lon"],
                    lat = shop["location"]["lat"]
                )
                db.add(new_shop_loc)
                
        """Commit the changes to the database"""
        db.commit()

    except SQLAlchemyError as sqla_error:
        logging.error("SQLAlchemy error occurred: {}".format(str(sqla_error)), exc_info=True)
        db.rollback()  # Rollback the transaction in case of an SQLAlchemy error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    except Exception as e:
        logging.error(
            f"An error occurred while saving the response: {e}", 
            exc_info=sys.exc_info()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    finally:
        db.close()