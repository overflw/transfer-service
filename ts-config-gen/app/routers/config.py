from typing import List, Optional, Any
from fastapi import APIRouter, Depends

from app.models.configmodel import ConfigBase, Config, ConfigInDB
from app.crud.config import configs
from app.db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter(
    prefix="/config",
    tags=["config"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get(
    '/',
    response_model=List[ConfigInDB],
    response_model_exclude_none=True,
    summary="Retrieve Transformation Configurations",
    description="You can retrieve transformation configuartions available on this instance"
)
async def get_config_multi(
    db: AsyncIOMotorClient = Depends(get_database),
    importingDatacontroller: Optional[str] = None,
    exportingDatacontroller: Optional[str] = None,
    sort: Optional[Any] = ('_id'),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    filter_query = None
    if importingDatacontroller:
        filter_query.update(
            {'importingDatacontroller': importingDatacontroller})
    if exportingDatacontroller:
        filter_query.update(
            {'exportingDatacontroller': exportingDatacontroller})

    return await configs.read_multi(db=db, filter=filter_query, sort=sort, skip=skip, limit=limit)


@router.get(
    '/{config_id}',
    response_model=ConfigInDB,
    response_model_exclude_none=True,
    summary="Retrieve a Transformation Configuration",
    description="You can retrieve a single transformation configuration available on this instance, by its id."
)
async def get_config(
    config_id: str,
    db: AsyncIOMotorClient = Depends(get_database),
) -> Any:
    print("config_id", config_id)
    return await configs.read(db, config_id)
