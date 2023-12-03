from fastapi import APIRouter, Depends
from ..controller import *
from .. import schemas
from ..middleware.verify_api_key import verify_api_key

router = APIRouter(
    prefix="/shop",
    tags = ["SHOP"]
)

router.add_api_route(
    "/", 
    get_shop, 
    response_model=schemas.ShopList, 
    methods=["GET"],
    dependencies=[Depends(verify_api_key)]
)

router.add_api_route(
    "/{id}", 
    get_shop_by_id, 
    response_model=schemas.Shop, 
    methods=["GET"],
    dependencies=[Depends(verify_api_key)]
)