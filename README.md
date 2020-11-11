# airflow-tutorial

## Prerequisite

* [Docker](https://docs.docker.com/desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

### Image Build

```
docker-compose build
```

### Start Services

```
docker-compose up -d
```

### Edit postgres connection

If you want to run dags `discord` and `parse_discord`, please edit `postgres_default` in airflow connection page.

```
Host: postgres
Schema: airflow
Login: airflow
Password: airflow
Port: 5432
```

## Remove

### Stop Services

```
docker-compose down
```

### Remove Files

```
rm -rf logs volume
```

## Known Issues

### Start Services error

We may get error after executing `docker-compose up -d`. Please run `docker-compose down` and run `docker-compose up -d` to start services again.
