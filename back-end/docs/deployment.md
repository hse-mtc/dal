# Deployment

Make sure that all the [instructions](environment.md)
for setting up the environment have been followed.

1. Navigate to the *project* root (directory with `back-end` and `front-end`):
   ```shell script
   cd dal
   ```

1. If models have changed, generate migrations:
   ```shell script
   docker-compose run back-end python manage.py makemigrations
   ```
   
1. Simply run (note that `front-end` is optional):
   ```shell script
   docker-compose up --build back-end [front-end]
   ```
