# DMS back-end

## Using Docker

```bash
docker-compose up
```

Back-end will be available at https://localhost:8000.


## Without Docker

### Installing Dependencies
Create new virtual environment:
```bash
python3 -m venv .venv
```

Activate it:
```bash
source .venv/bin/activate
```

Install requirements using `pip`:
```bash
pip install -r requirements.txt
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
