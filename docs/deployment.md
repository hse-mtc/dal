# Deployment

Make sure that all the [instructions](environment.md) for setting up the environment have been followed.

Navigate to the project root:
```shell script
cd dms-back
```

## With Docker

Simply run:
```shell script
docker-compose up --build
```

Note that your `.env` file will be overwritten by `.env.example`.

## Manual

Make database migrations:
```shell script
python manage.py makemigrations && python manage.py migrate
```

Run the server:
```shell script
python manage.py runserver 0.0.0.0:$DMS_PORT
```