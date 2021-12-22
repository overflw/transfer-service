from typing import List, Union, Optional, Any
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.config_gen.utils import generate_config

from app.models.requestmodel import RequestBase, Request, RequestInDB
from app.crud.config import configs
from app.db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter(
    prefix="/generate",
    tags=["generate"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post(
    '/',
    response_model=Any,
    response_model_exclude_none=True,
    summary="Issue a config generation",
    description="You can generate a config by submitting two data controler URLs."
)
async def submit_generation_request(
    request: RequestBase = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
) -> Any:

    export_url: str = request.exportingDataControllerURL
    import_url: str = request.importingDataControllerURL
    repository_url: str = request.repositoryURL
    filter_query = {
        "exportingDataController": export_url,
        "importingDataController": import_url
    }

    # check whether a configuration already exists in db
    config_from_db = await configs.read_multi(db=db, filter=filter_query)
    if len(config_from_db) > 0:
        return config_from_db[0]

    # generate configuration
    config = generate_config(
        export_url=export_url, 
        import_url=import_url,
        repository_url=repository_url
        )

    # submit configuration in db
    await configs.create(db=db, obj_in=config)

    # send configuration to requesting server
    return config
