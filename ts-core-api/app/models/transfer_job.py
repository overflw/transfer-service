from typing import List, Optional
from pydantic import BaseModel, EmailStr, Extra, Field
from .rwmodel import RWModel
from .dbmodel import DateTimeModelMixin, DBModelMixin


class TransferJobBase(RWModel):
    exportingDataController: str = Field(..., example="https://exportingDataController.tld")
    importingDataController: str = Field(..., example="https://importingDataController.tld")
    exportingDataControllerUserId: str = Field(..., example="123456789", alias="UserId")

# Add optional created and updated timestamps
class TransferJob(DateTimeModelMixin, TransferJobBase):
    pass

# Add optional id information
class TransferJobInDB(DBModelMixin, TransferJob):
    pass
