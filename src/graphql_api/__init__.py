import strawberry

from strawberry.asgi import GraphQL
from src.resolvers.books.resolve_books import (
    resolve_create_book, resolve_get_book_by_id, resolve_get_book_by_isbn,
    resolve_update_book, resolve_delete_book
)


@strawberry.type
class Query:
    get_book_by_id = strawberry.field(resolve_get_book_by_id)
    get_book_by_isbn = strawberry.field(resolve_get_book_by_isbn)


@strawberry.type
class Mutation:
    create_book = strawberry.mutation(resolve_create_book)
    update_book = strawberry.mutation(resolve_update_book)
    delete_book = strawberry.mutation(resolve_delete_book)



schema = strawberry.Schema(query=Query(), mutation=Mutation())
graphql_app = GraphQL(schema, debug=True,)

