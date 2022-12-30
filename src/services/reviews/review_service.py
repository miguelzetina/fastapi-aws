import strawberry
from bson import ObjectId

from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from src.clients.db import (
    get_record, create_record, delete_record, get_and_update_record
)
from src.models.common.response_models import (
    CreateResponse, GetResponse, DeleteResponse, UpdateResponse
)
from src.models.db.db_models import DatabaseCollectionTypes
from src.models.reviews.review_models import Review


async def get_review_by_id(review_id: strawberry.ID) ->GetResponse[Review]:
    result = await get_record(
        DatabaseCollectionTypes.REVIEWS.value,
        {"_id": ObjectId(review_id)}
    )

    return GetResponse[Review](
        result=Review.from_dict(result),
        error_message=None,
        success=True
    )


async def create_review(review: Review) -> CreateResponse[Review]:
    new_review = review.to_dict()
    result: InsertOneResult = await create_record(
        DatabaseCollectionTypes.REVIEWS.value,
        new_review
    )
    if result is None:
        review_response = CreateResponse[Review](
            result=None,
            error_message="An error ocurred during review creation.",
            success=False
        )
    else:
        new_review["_id"] = result.inserted_id
        review_response = CreateResponse[Review](
            result=Review.from_dict(new_review),
            error_message=None,
            success=True
        )

    return review_response


async def update_review(review_id: strawberry.ID,
                        updated_review: dict) -> UpdateResponse[Review]:
    result: UpdateResult = await get_and_update_record(
        DatabaseCollectionTypes.REVIEWS.value,
        {"_id": ObjectId(review_id)},
        {"$set": updated_review}
    )

    if result is not None:
        review_response = UpdateResponse[Review](
            result=None,
            error_message="An error occurred updating the review.",
            success=False
        )
    else:
        review_response = UpdateResponse[Review](
            result=Review.from_dict(result),
            error_message=None,
            success=True
        )

    return review_response


async def delete_review(review_id: strawberry.ID) -> DeleteResponse[Review]:
    delete_result: DeleteResult = await delete_record(
        DatabaseCollectionTypes.REVIEWS.value,
        {"_id": review_id}
    )

    delete_response = DeleteResponse[Review](
        result=delete_result,
        record_id=review_id,
        error_message=None,
        success=True
    )

    return delete_response

