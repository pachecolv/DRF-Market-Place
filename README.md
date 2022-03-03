# DRF-Market-Place
Market place implementation using django rest framework (DRF)

An user can sign up either as a buyer or a seller. Sellers can add to the platform products they would like to sell.
The buyers can see all products in the market place and decide which one they would like to purchase.

When a transaction is completed, the quantity of available product units and the seller balance are updated.

Users also have the option to add products they are interested in to a wish list.

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
