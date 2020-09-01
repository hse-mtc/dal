# DMS back end

## Development

### Setting up

For ease of development, it is recommended to set up the IDE environment 
by following the detailed instructions [here](docs/ide.md).

## Deployment

## Using Docker

```bash
docker-compose up
```

Back-end will be available at https://localhost:8000.


## Without Docker

### Installing Dependencies
Install required Python version using `pyenv`:
```bash
pyenv install 3.8.1
```

Activate `pipenv`:
```bash
pipenv shell
```

If pipenv doesn't install dependencies from Pipfile, use:
```bash
pipenv sync
```


### Local Postgres Database
(Virtual environment must be activated.)

Create new database and open it using `psql`:

```bash
createdb db_name
psql db_name
```

Create new user with password:
```psql
CREATE USER db_user WITH PASSWORD 'db_user_password';
\q
```

Synchronize the database state using Django's `migrate`:
```bash
python manage.py migrate
```


### Running Backend Server
(Virtual environment must be activated.)

```bash
python manage.py runserver
```
