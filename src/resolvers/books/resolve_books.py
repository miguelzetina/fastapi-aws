import datetime

from bson import ObjectId

from src.models.authors.author_models import AuthorInput
from src.models.books.book_models import Book
from src.models.common.response_models import (
    GetResponse, CreateResponse, UpdateResponse, DeleteResponse
)
from src.services.books import book_service


async def resolve_get_book_by_id(bookd_id: str) -> GetResponse[Book]:
    return await book_service.resolve_get_book_by_id(ObjectId(book_id))


async def resolve_get_book_by_isbn(isbn: str) -> GetResponse[Book]:
    return await book_service.resolve_get_book_by_isbn(ObjectId(isbn))


async def resolve_create_book(title: str, author: AuthorInput, price: float,
                              subtitle: str = None, description: str: None,
                              isbn: str = None, book_format: str = None)
                              -> CreateResponse[Book]:
    new_book = Book(None, title, author, price, subtitle, description, isbn,
                    book_format, None, False, datetime.datetime.now(), None)
    return await book_service.resolve_create_book(new_book)

