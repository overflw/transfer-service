from typing import Any, List
from fastapi import APIRouter, Depends, Body

from app.models.transfer_job import TransferJobInDB, TransferJobBase
from app.translator.utils import request_translation_config, translate_data
from app.data_transfer.core import start_transfer
from app.crud.transfer import transfer_crud
from app.crud.data_disclosed import data_disclosed_crud
from app.db.mongodb import AsyncIOMotorClient, get_database


router = APIRouter(
    prefix="/transfer",
    tags=["transfer"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "Success"}
    },
)


@router.get(
    '/{job_id}',
    response_model=TransferJobInDB,
    summary="Retrieve tranfer job",
    description="Retrive a transfer job, by its id, for the current user"
)
async def get_transfer_job(
    job_id: str,
    db: AsyncIOMotorClient = Depends(get_database),
) -> Any:
    return await transfer_crud.read(db, job_id)


@router.get(
    '/',
    response_model=List[TransferJobInDB],
    summary="Retrieve tranfer jobs",
    description="Retrive all transfer jobs for the current user"
)
async def retrieve_all_transfer_jobs(
    db: AsyncIOMotorClient = Depends(get_database)
) -> Any:
    return await transfer_crud.read_multi(db)


@router.post(
    '/',
    response_model=TransferJobInDB,
    summary="Submit new tranfer job",
    description="Submit a new tranfer job for the current user"
)
async def post_transfer_job(
    job: TransferJobBase = Body(...),
    db: AsyncIOMotorClient = Depends(get_database)
) -> Any:

    # Create a new transfer job and submit it to the db
    created_job = await transfer_crud.create(db=db, doc_in=job)

    # Retrieve translation config
    translation_config = await request_translation_config(job)

    # Retrieve the data disclosed for the current user
    filter = {"user_id": job.exportingDataControllerUserId}
    source_data = data_disclosed_crud.read(db, filter=filter)

    # Apply translation config to the source data of the requesting user
    translated_data = await translate_data(source_data, translation_config)

    # Try to transfer the data to target data controller
    start_transfer(job.importingDataController, translated_data)

    return created_job
