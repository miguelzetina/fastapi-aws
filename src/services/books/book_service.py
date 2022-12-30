from typing import List

import strawberry

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from src.clients.db import (
    get_record, create_record, get_and_update_record, delete_record,
    get_records, build_bulk_avg_value_pipeline
)
from src.models.books.book_models import Book
from src.models.common.response_models import (
    CreateResponse, DeleteResponse, GetResponse, UpdateResponse
)
from src.models.db.db_models import DatabaseCollectionTypes, BulkRecordUpdateResponse


async def get_book_by_id(book_id: strawberry.ID) -> GetResponse[Book]:
    result = await get_record(DatabaseCollectionTypes.BOOKS.value,
                              {"_id": ObjectId(book_id)})

    return GetResponse[Book](result=Book.from_dict(result),
                             error_message=None,
                             success=True)


async def get_book_by_isbn(isbn: str) -> GetResponse[Book]:
    result = await get_record(DatabaseCollectionTypes.BOOKS.value, {"isbn":
                                                                    isbn})
    return GetResponse[Book](result=Book.form_dict(result), error_message=None,
                             success=True)


async def create_book(book: Book) -> CreateResponse:
    new_book = book.to_dict()
    result: InsertOneResult = await create_record(
        DatabaseCollectionTypes.BOOKS.value,
        new_book
    )
    if result is None or result.inserted_id is None:
        book_response = CreateResponse[Book](
            result=None,
            error_message="An error ocurred during book creation.",
            success=False
        )
    else:
        new_book["_id"] = result.inserted_id
        book_response = CreateResponse[Book](
            result=Book.from_dict(new_book),
            error_message=None,
            success=True
        )
    return book_response


async def update_book(book_id: strawberry.ID,
                      updated_book: dict) ->UpdateResponse[Book]:

    result: UpdateResult = await get_and_update_record(
        DatabaseCollectionTypes.BOOKS.value,
        {"_id": ObjectId(book_id)},
        {"$set": updated_book}
    )
    if result is None:
        book_response = UpdateResponse[Book](
            result=None,
            error_message="An error ocurred during book update.",
            success=False
        )
    else:
        book_response = UpdateResponse[Book](
            result=Book.from_dict(result),
            error_message=None,
            success=True
        )
    return book_response


async def delete_book(book_id: strawberry.ID) -> DeleteResponse[Book]:
    delete_result: DeleteResult = await delete_record(
        DatabaseCollectionTypes.BOOKS.value,
        {"_id": ObjectId(book_id)}
    )

    delete_response = DeleteResponse[Book](result=delete_result,
                                           record_id=book_id,
                                           error_message=None,
                                           success=True)

    return delete_response


async def get_books_to_update() -> List[str]:
    result = await get_records(
        DatabaseCollectionTypes.BOOKS.value,
        {"asyncUpdateRequired": True}
    )
    books = []
    async for doc in result:
        books.append(str(doc['_id']))

    return books


async def bulk_update_book_ratings() -> BulkRecordUpdateResponse:
    books = await get_books_to_update()
    raiting_responses = await get_bulk_avg_reservation_rating_by_book_ids(books)

    bulk_results = []
    for rating_response in rating_responses:
        result: UpdateResponse[Book] = await update_book(
            rating_response['_id'],
            {
                'rating': rating_response['avg_rating'],
                'asyncUpdateRequired': False,
                'lastUpdatedOn': datetime.datetime.now()
            }
        )

        bulk_results.append(result)

    return BulkRecordUpdateResponse(bulk_results)


async def get_bulk_avg_reservation_rating_by_book_ids(book_ids: List[str]) -> List[dict]:
    pipeline = build_bulk_avg_value_pipeline("bookId", book_ids, "rating")

    cursor = await aggregate(DatabaseCollectionTypes.REVIEWS.value, pipeline)
    results = await cursor.to_list(length=1000)

    return results

