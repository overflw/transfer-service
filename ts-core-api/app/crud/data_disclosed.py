
from app.models.data_disclosed import ItemInDB, ItemBase
from app.core.config import database_name, data_disclosed_collection
from app.crud.base import CRUDBase


class CRUDDataDis(CRUDBase[ItemBase, ItemBase, ItemInDB]):
    pass


data_disclosed_crud = CRUDDataDis(
    model=ItemInDB,
    database_name=database_name,
    collection_name=data_disclosed_collection
)
