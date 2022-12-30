import strawberry
from bson import ObjectId

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from src.clients.db import (
    get_record, create_record, get_and_update_record, delete_record
)
from src.models.books.book_models import Book
from src.models.common.response_models import (
    CreateResponse, DeleteResponse, GetResponse, UpdateResponse
)
from src.models.db.db_models import DatabaseCollectionTypes


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

