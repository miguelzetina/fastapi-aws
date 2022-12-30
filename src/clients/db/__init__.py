from typing import List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings


mongo_client: AsyncIOMotorClient

db_url = settings.DB_URL
db_name = settings.DB_NAME


def get_db() -> AsyncIOMotorDatabase:
    return AsyncIOMotorClient(db_url)[db_name]


# Record Retrieval Helper Functions
async def get_record(collection: str, query:dict) -> dict:
    # if object has a null id as well as _id
    # then change to get_db()[collection].find_one(query, {'id': False})
    return await get_db()[collection].find_one(query)


async def get_record_count(collection: str, query:dict) -> dict:
    return await get_db()[collection].count_documents(query)


async def agregate(collection: str, pipeline:list[dict]) -> dict:
    return get_db()[collection].aggregate(pipeline=pipeline, allowDiskUse=True)


async def get_records(collection: str, query:dict, projection: dict = None):
    return get_db()[collection].find(query, projection)


async def get_records_with_pagination(collection: str,
                                      query:dict,
                                      pagination_info: dict,
                                      limit: int) -> dict:
    return get_db()[collection]\
            .find(query)\
            .skip(pagination_info['skip'])\
            .limit(limit)


# Record Creation and Updating Helper Functions
async def create_record(collection: str,
                        query: dict) -> dict:
    if '_id' in query:
        del query['_id']
    return await get_db()[collection].insert_one(query)


async def update_record(collection: str,
                        object_query: dict,
                        update_query: dict) -> dict:
    if '_id' in update_query:
        del update_query['_id']
    return await get_db()[collection].update_one(object_query, update_query)


async def get_and_update_record(collection: str,
                                object_query: dict,
                                update_query: dict) -> dict:
    if '_id' in update_query:
        del update_query['_id']
    return await get_db()[collection].find_one_and_update(object_query,
                                                          update_query)


# Record Deletion Helper Functions
async def delete_record(collection: str,
                        query: dict) -> dict:
    return await get_db()[collection].delete_one(query)


async def delete_all_records(collection:str,
                             query: dict) -> dict:
    return await get_db()[collection].delete_many(query)


def build_bulk_avg_value_pipeline(field_to_match: str,
                                  field_values_to_match: List[object],
                                  field_to_calculate_average: str) -> List[dict]:
    return [
        {'$match': {field_to_match: {"$in": field_values_to_match}}},
        {'$group':
            {
                '_id': '$' + field_to_match,
                'avg_rating': {'$avg': '$' + field_to_calculate_average}
            }
        }
    ]

