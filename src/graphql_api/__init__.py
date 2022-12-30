import strawberry

from strawberry.asgi import GraphQL
from src.resolvers.books.resolve_books import (
    resolve_create_book, resolve_get_book_by_id, resolve_get_book_by_isbn,
    resolve_update_book, resolve_delete_book
)
from src.resolvers.reviews.resolve_reviews import (
    resolve_create_review, resolve_get_review_by_id
)


@strawberry.type
class Query:
    # Book Queries
    get_book_by_id = strawberry.field(resolve_get_book_by_id)
    get_book_by_isbn = strawberry.field(resolve_get_book_by_isbn)
    # Review Queries
    get_review_by_id = strawberry.field(resolve_get_review_by_id)


@strawberry.type
class Mutation:
    # Book Create, Update, and Delete Mutations
    create_book = strawberry.mutation(resolve_create_book)
    update_book = strawberry.mutation(resolve_update_book)
    delete_book = strawberry.mutation(resolve_delete_book)
    # Review Create, Update, and Delete Mutations
    create_review = strawberry.mutation(resolve_create_review)
    update_review = strawberry.mutation(resolve_update_review)
    delete_review = strawberry.mutation(resolve_delete_review)


schema = strawberry.Schema(query=Query(), mutation=Mutation())
graphql_app = GraphQL(schema, debug=True,)

