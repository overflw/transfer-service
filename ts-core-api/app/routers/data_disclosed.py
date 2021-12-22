from typing import List, Union
from fastapi import APIRouter, Depends, Body

from app.models.data_disclosed import *
from app.crud.data_disclosed import data_disclosed_crud
from app.db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter(
    prefix="/datadisclosed",
    tags=["datadisclosed"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "Success"}
    }
)


@router.get(
    '/',
    response_model=List[ItemInDB],
    response_model_exclude_none=True,
    summary="Retrieve data disclosed items",
    description="You can retrieve data disclosed items available on this TS instance"
)
async def get_item_multi(
    db: AsyncIOMotorClient = Depends(get_database),
    sort: Optional[Any] = ('_id'),
    skip: int = 0,
    limit: int = 100,
    filterQuery = None
) -> Any:

    return await data_disclosed_crud.read_multi(db=db, filter=filterQuery, sort=sort, skip=skip, limit=limit)

@router.post(
    '/',
    response_model=ItemBase,
    response_model_exclude_none=True,
    summary="",
    description=""
)
async def post_item(
    itemIn: ItemBase = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
) -> Any:

    return await data_disclosed_crud.create(db=db, doc_in=itemIn)