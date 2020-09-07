# Deployment

Make sure that all the [instructions](environment.md)
for setting up the environment have been followed.

Navigate to the project root:
```shell script
cd backend
```

## Docker

Simply run:
```shell script
docker-compose --env-file .env.docker up --build
```

Note that settings will be taken from [`.env.docker`](../.env.docker).

## Local Machine

Virtual environment must be active and 
any changes to `.env` file must be followed by reloading it:
1. If venv is active, exit from it:
   ```shell script
   exit
   ```
1. Run shell with venv again: 
   ```shell script
   pipenv shell
   ```

If models have changed,
make database migrations:
```shell script
python manage.py makemigrations
```

If there are new migrations (from your changes or pulled from repo),
apply them:
```shell script
python manage.py migrate
```

Run the server:
```shell script
python manage.py runserver localhost:$DAL_PORT
```
