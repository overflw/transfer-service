from typing import Optional, Any
from pydantic import BaseModel, Extra, Field
from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId


class RequestBase(RWModel):
    exportingDataControllerURL: str = Field(..., example="https://exportingDataController.tld")
    importingDataControllerURL: str = Field(..., example="https://importingDataController.tld")
    repositoryURL: Optional[str] = Field(None, example="https://repository.tld")


class Request(DateTimeModelMixin, RequestBase):
    # Add optional created and updated timestamps
    pass


class RequestInDB(DBModelMixin, Request):
    # Add optional id information
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        description='The id of a request. The id is necessary to distinguish several processing tasks of the same request (locally unique ID that can be based on the database implementation).',
        examples=['f1424f86-ca0f-4f0c-9438-43cc00509931'],
        title='_id',
        alias='_id'
    )
