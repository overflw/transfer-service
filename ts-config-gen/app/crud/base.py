from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from bson import ObjectId


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DBSchemaType = TypeVar("DBSchemaType", bound=BaseModel)

# TODO: Any -> concrete Type

class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType, DBSchemaType]):
    def __init__(
        self, 
        model: Type[DBSchemaType], 
        collection_name: str,
        database_name: str = "ts_config"
        ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic model (schema) class
        * `collection_name`: A MongoDB collection name
        * `database_name`: A MongoDB database name
        """
        self.model = model
        self.database_name = database_name
        self.collection_name = collection_name

    async def read(self, db: Any, db_doc_id: str) -> Optional[DBSchemaType]:
        
        # TODO Implement filter
        coll = db[self.database_name][self.collection_name]
        oId = ObjectId(db_doc_id)
        print("oId:",oId)
        document = await coll.find_one({"_id": oId})
        print("document",document)
        return self.model(**document)

    async def read_multi(
        self,
        db: Any,
        *,
        filter: object = None,
        sort: Any = ('_id'),
        skip: int = 0,
        limit: int = 100
    ) -> List[DBSchemaType]:

        coll = db[self.database_name][self.collection_name]
        documents = []
        cursor = coll.find(filter)
        cursor.sort(sort).skip(skip).limit(limit)

        async for document in cursor:
            documents.append(
                self.model(**document)
            )

        return documents

    async def create(
        self,
        db: Any,
        *,
        doc_in: CreateSchemaType
    ) -> DBSchemaType:

        coll = db[self.database_name][self.collection_name]
        doc_in_data = jsonable_encoder(doc_in)
        now = datetime.datetime.now()
        db_obj = self.model(
            **doc_in_data,
            createdAt=now,
            updatedAt=now
        )  # type: ignore
        # if isinstance(doc_in, dict):...
        db_obj = await coll.insert_one(db_obj.dict())
        db_doc_inserted = await coll.find_one({"_id": db_obj.inserted_id})

        return self.model(**db_doc_inserted)

    async def update(
        self,
        db: Any,
        *,
        db_doc_id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> DBSchemaType:

        coll = db[self.database_name][self.collection_name]
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        db_doc = self.read(coll, db_doc_id)
        db_doc_data = jsonable_encoder(db_doc)

        for field in db_doc_data:
            if field in update_data:
                setattr(db_doc, field, update_data[field])
        
        result = await coll.replace_one({'_id': db_doc._id}, db_doc)
        db_doc_updated = await coll.find_one({'_id': db_doc._id})
        return self.model(**db_doc_updated)

    async def delete(
        self, 
        db: Any, 
        *, 
        db_doc_id: str
        ):

        coll = db[self.database_name][self.collection_name]
        db_doc = self.read(coll, db_doc_id)
        result = await coll.delete({'_id': db_doc._id})

        return db_doc
