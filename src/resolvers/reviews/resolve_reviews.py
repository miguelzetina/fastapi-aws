import datetime

from bson import ObjectId

from src.models.common.response_models import (
    GetResponse, CreateResponse, UpdateResponse, DeleteResponse
)
from src.models.reviews.review_models import Review
from src.services.reviews import review_service


async def resolve_get_review_by_id(review_id: str) -> GetResponse[Review]:
    return await review_service.get_review_by_id(ObjectId(review_id))


async def resolve_create_review(book_id: str,
                                reviewer_id: str,
                                rating: float,
                                review_comments: str = None) \
        -> CreateResponse[Review]:
    new_review = Review(None, book_id, reviewer_id, rating, review_comments,
                        datetime.datetime.now(), None)

    return await review_service.create_review(new_review)

