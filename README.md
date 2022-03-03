# DRF-Market-Place
Market place implementation using django rest framework (DRF)

## Running the project


This project uses docker containers to run the API and the postgres database. 
To create and run the containers for the first time, run:
```
docker-compose up --build
```

It is necessary to apply database migrations before serving any http requests.
```
docker exec -it market-place-api pipenv run python manage.py migrate
```

Once migrations have been applied, restart the market-place-api container:
```
docker container restart market-place-api
```

## Running tests

This project comes with a few implemented tests. To run them:
```
docker exec -it market-place-api pipenv run python manage.py test
```
## Authentication

This project uses JWT tokens for authentication. The token is required for all endpoints, except for signing up.
An access token can be obtained through the `/token/` endpoint. A refresh token endpoint is implemented at `/token/refresh/`.
