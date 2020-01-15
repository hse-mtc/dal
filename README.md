# military-dms

## Installing Dependencies
```
$ virtualenv --python=<path/to/python3.7.4> .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Local Postgres Database
```
$ createdb db_name
$ psql db_name

    db_name=# CREATE USER db_user WITH PASSWORD 'db_user_password';
    db_name=# \q
    
$ python manage.py migrate
$ python manage.py runserver
```
