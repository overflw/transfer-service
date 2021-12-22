from datetime import datetime, timezone

from pydantic import BaseConfig, BaseModel
from bson import ObjectId


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            ObjectId: str
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True