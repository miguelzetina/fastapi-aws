FROM python:3.10.9-bullseye

# Install Environment Dependencies
RUN pip install fastapi uvicorn poetry wheel virtualenv

EXPOSE 8000

# set working directory
WORKDIR /usr/src/bookapi

# set environment variables
ENV PORT 8000
ENV HOST "0.0.0.0"
ENV DB_URL="mongodb://db:27017"
ENV DB_NAME="bookapi"

# Copy Required Project Assets
COPY ./src/ /bookapi/src
COPY ./main.py /bookapi
COPY ./pyproject.toml /bookapi

# Change directories
WORKDIR /bookapi

# Install Project Dependencies
RUN poetry config virtualenvs.create false && poetry install

# Entry Point
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

