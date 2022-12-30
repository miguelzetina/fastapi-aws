from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uvicorn, datetime

from src.config import settings
from src.graphql_api import graphql_app
from src.jobs.book_ratings_job import update_average_book_ratings


app = FastAPI()
app.mount('/graph', graphql_app)


@app.on_event('startup')
@repeat_every(seconds=60 * 60 * 24)
async def mass_update_book_ratings() -> None:
    """Scheduled job used to update book ratings"""
    await update_average_book_ratings()


@app.on_event('startup')
async def startup():
    public_paths = {'/', '/graph/'},


@app.get("/")
async def root():
    return {
        "message": {
            "app_name": settings.APP_NAME,
            "system_time": datetime.datetime.now()
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=True,
        port=settings.PORT,
    )

