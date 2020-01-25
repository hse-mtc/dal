# Military DMS

## Using Docker

```
$ docker-compose up
```

Back-end will be available at https://localhost:8000.


## Without Docker

### Installing Dependencies
Create new virtual environment using `virtualenv`:
```
$ virtualenv --python=<path/to/python3.7.4> .venv
```

Another way:
```
$ <path/to/python3.7.4> -m venv .venv
```

Activate it:
```
$ source .venv/bin/activate
```

Install requirements using `pip`:
```
$ pip install -r requirements.txt
```


### Local Postgres Database
(Virtual environment must be activated.)

Create new database and open it using `psql`:

```
$ createdb db_name
$ psql db_name
```

Create new user with password:
```
db_name=# CREATE USER db_user WITH PASSWORD 'db_user_password';
db_name=# \q
```

Change database settings to local in `djangoherokuapp/settings.py`:
```
    ...
    DATABASE_SETTINGS = 'local'
    ...
```

Synchronize the database state using Django's `migrate`:
```
$ python manage.py migrate
```


### Running Backend Server
(Virtual environment must be activated.)

```
$ python manage.py runserver
```
