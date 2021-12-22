
from app.models.configmodel import ConfigInDB, ConfigBase
from app.core.config import database_name, config_collection
from app.crud.base import CRUDBase


class CRUDconfig(CRUDBase[ConfigBase, ConfigBase, ConfigInDB]):
    pass


configs = CRUDconfig(
    model=ConfigInDB,
    database_name=database_name,
    collection_name=config_collection
)
