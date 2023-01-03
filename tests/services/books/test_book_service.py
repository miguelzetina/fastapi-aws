from datetime import datetime
from unittest import mock

import pytest
from pymongo.results import InsertOneResult, DeleteResult
from bson import ObjectId

from src.models.authors.author_models import Author
from src.models.books.book_models import Book
from src.services.books import book_service

from tests.test_utils.test_data import get_book_records


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.create_record")
async def test_create_book(mock_create_record):
    mock_create_record.return_value = InsertOneResult(
        inserted_id="61c254f4f2931ef2972ef812", acknowledged=True
    )

    new_book = Book(
        _id=None,
        title="Test Book",
        author=Author("Fake", "Author", None),
        price=9.99,
        subtitle="subtitle",
        description="description",
        isbn=9781234567812,
        book_format="paperback",
        rating=None,
        async_update_required=False,
        created_on=None,
        last_updated_on=None,
    )

    create_response = await book_service.create_book(new_book)

    assert create_response is not None
    assert create_response.result.author.first_name.__contains__("Fake")
    assert create_response.result.author.last_name.__contains__("Author")


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_and_update_record")
async def test_update_book(mock_update_record):
    mock_update_record.return_value = get_book_records()[0]

    new_book_values = {
        "title": "Updated Title",
        "subtitle": "Updated Subtitle",
        "format": "ebook",
        "lastUpdatedOn": datetime.now(),
    }

    update_response = await book_service.update_book(
        ObjectId("620fdbb0cf1be3116b86ad77"), new_book_values
    )

    assert update_response is not None
    assert update_response.result.author.first_name.__contains__("Fake")
    assert update_response.result.author.last_name.__contains__("Author")
    assert update_response.result.author.middle_name is None
    assert update_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.delete_record")
async def test_delete_book(mock_delete_record):
    mock_delete_record.return_value = DeleteResult(
        raw_result={"record_deleted": 0}, acknowledged=True
    )

    delete_response = await book_service.delete_book(
        ObjectId("620fdbb0cf1be3116b86ad77")
    )

    assert delete_response is not None
    assert delete_response.success is True
    assert delete_response.record_id is not None


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.create_record")
async def test_create_book_failure(mock_create_record):
    mock_create_record.return_value = InsertOneResult(
        inserted_id=None, acknowledged=False
    )

    new_book = Book(
        _id=None,
        title="Test Book",
        author=Author("Fake", "Author", None),
        price=9.99,
        subtitle="subtitle",
        description="description",
        isbn=9781234567812,
        book_format="paperback",
        rating=None,
        async_update_required=False,
        created_on=None,
        last_updated_on=None,
    )

    create_response = await book_service.create_book(new_book)

    assert create_response is not None
    assert create_response.success is False
