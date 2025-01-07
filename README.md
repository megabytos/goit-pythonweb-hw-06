# Python Web Development HW 6 - SQLAlchemy, Alembic

## Setup environment

Rename .env_example to .env and edit the database credentials if necessary

```shell
mv .env_example .env
```
Run docker container with Postgres Database

```shell
sh ./postgres.sh
```
Install project dependencies

```shell
poetry install
```
Activate virtual environment

```shell
poetry shell
```
## Setup database

Create database migrations

```shell
alembic revision --autogenerate -m 'Init'
```
Apply database migrations

```shell
alembic upgrade head
```
Seed the database with fake data
```shell
python seed.py
```
## Run sample queries
```shell
python my_select.py
```

## Cleanup data

Clear database
```shell
alembic downgrade base
```

Remove all migrations
```shell
rm -r migrations/versions/*
```

Stop the Postgres Docker container
```shell
docker stop Postgres-hw06
```
Remove the Postgres Docker container
```shell
docker rm Postgres-hw06
```
