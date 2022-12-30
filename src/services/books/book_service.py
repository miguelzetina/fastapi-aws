import strawberry
from bson import ObjectId

from pymongo.results impot InsertOneResult

from src.clients.db import get_record, create_record
from src.models.books.book_models import Book
from src.models.common.response_models import CreateResponse, GetResponse
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
    result: InsertOneResult = await
    create_record(DatabaseCollectionTypes.BOOKS.value, new_book)
    if result is None or result.inserted_id is None:
        book_response = CreateResponse[Book](result=None, error_message="An
                                             error ocurred during book
                                             creation.",
                                             success=False)
    else:
        new_book["_id"] = result.inserted_id
        book_response = CreateResponse[Book](
            result=Book.from_dict(new_book),
            error_message=None,
            success=True)
    return book_response

