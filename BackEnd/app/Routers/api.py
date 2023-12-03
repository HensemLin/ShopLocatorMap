from fastapi import status, APIRouter
from typing import List

from .. import schemas
from ..controller import *

router = APIRouter(
    prefix="/API",
    tags = ["API KEY"]
)

router.add_api_route(
    "/", 
    get_api_key, 
    response_model=List[schemas.ApiKeyOut], 
    methods=["GET"]
)

router.add_api_route(
    "/{id}", 
    get_api_key_by_id, 
    response_model=schemas.ApiKeyOut, 
    methods=["GET"]
)

router.add_api_route(
    "/createAPI/", 
    create_api_key, 
    response_model=schemas.ApiKeyOut, 
    status_code=status.HTTP_201_CREATED,
    methods=["GET"]
)

router.add_api_route(
    "/{id}", 
    delete_api_key, 
    status_code=status.HTTP_204_NO_CONTENT,
    methods=["DELETE"],
)