from typing import Optional, Any
from pydantic import BaseModel, Extra, Field
from app.models.rwmodel import RWModel
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId


class ConfigBase(RWModel):
    exportingDataController: str = Field(..., example='https://exportingDataController.tld')
    importingDataController: str = Field(..., example='https://importingDataController.tld')
    config: dict = Field(..., example={
        'key': 'source data path with transformation rules'
    })


class Config(DateTimeModelMixin, ConfigBase):
    # Add optional created and updated timestamps
    pass


class ConfigInDB(DBModelMixin, Config):
    # Add optional id information
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        description='The id of a Config. The id is necessary to distinguish several processing tasks of the same Config (locally unique ID that can be based on the database implementation).',
        examples=['f1424f86-ca0f-4f0c-9438-43cc00509931'],
        title='_id',
        alias='_id'
    )
