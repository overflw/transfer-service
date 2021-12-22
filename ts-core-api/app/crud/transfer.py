
from app.models.transfer_job import TransferJob, TransferJobInDB, TransferJobBase
from app.core.config import database_name, transfer_job_collection
from app.crud.base import CRUDBase


class CRUDTransfer(CRUDBase[TransferJobBase, TransferJobBase, TransferJobInDB]):
    pass


transfer_crud = CRUDTransfer(
    model=TransferJobInDB,
    database_name=database_name,
    collection_name=transfer_job_collection
)