FROM python:3.8-slim-buster

# Install dependencies
RUN apt-get update -yy \
    && apt-get upgrade -yy \
    && apt-get install -yy libpq-dev gcc \
    && pip install --no-cache-dir pipenv

# Add project files and configure workdir
COPY ./django_api /django_api
WORKDIR /django_api/market_place

RUN pipenv install --pre