import sys
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
from ...database import db_models
from ...database.db_setup import get_db
from ... import schemas


async def get_shop(db: Session = Depends(get_db)):
    """
    Retrieves a list of shops and their locations from the database.

    Args:
        db (Session): The database session.

    Returns:
        ShopList: A list of shop details including their locations and the center of all shops.

    Raises:
        HTTPException: If no shops are found, a 404 Not Found Error is raised.
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try: 
        """Query the database to join Shop and ShopLocation tables and retrieve all records."""
        shops = db.query(db_models.Shop, db_models.ShopLocation)\
                .join(db_models.ShopLocation, db_models.Shop.id == db_models.ShopLocation.shopId)\
                .all()
        
        "If no shops are found, raise a 404 Not Found error."
        if not shops:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No shop(s) found"
            )

        shops_list = []
        avg_lat = 0
        avg_lon = 0

        """Iterate through the shops and their locations."""
        for shop, location in shops:
            avg_lat += location.lat     # Add the latitude to the total for averaging.
            avg_lon += location.lon     # Add the longitude to the total for averaging.

            loc = schemas.ShopLocation(
                lat=location.lat,
                lon=location.lon
            )
            shop = schemas.Shop(
                id=shop.id,
                name=shop.name,
                address=shop.address,
                location=loc
            )
            shops_list.append(shop)

        """Calculate the center location of all shops."""
        center = schemas.center(
            lat=avg_lat/len(shops),
            lon=avg_lon/len(shops)
        )

        result = schemas.ShopList(
            shop=shops_list,
            center=center
        )

        return result
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=sys.exc_info())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def get_shop_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single shop and its location from the database based on the given ID.

    Args:
        id (int): The ID of the shop to retrieve.
        db (Session): The database session.

    Returns:
        Shop: The shop details including its location.

    Raises:
        HTTPException: If the specified shop is not found, a 404 Not Found Error is raised.  
        HTTPException: If any other unexpected error occurs, a 500 Internal Server Error is raised.
    """
    try: 
        """Query the database to join Shop and ShopLocation tables 
        and retrieve the first record that matches the given shop ID."""
        shops = db.query(db_models.Shop, db_models.ShopLocation)\
                .join(db_models.ShopLocation, db_models.Shop.id == db_models.ShopLocation.shopId)\
                .filter(db_models.Shop.id==id).first()
        
        """If the shops is not found, raise a 404 Not Found error"""
        if not shops:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No shop(s) found"
            )

        """Unpack the query result into shop and location variables."""
        shop, location = shops
        
        loc = schemas.ShopLocation(
                lat=location.lat,
                lon=location.lon
            )
        combined = schemas.Shop(
                id=shop.id,
                name=shop.name,
                address=shop.address,
                location=loc
            )

        return combined
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=sys.exc_info())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )