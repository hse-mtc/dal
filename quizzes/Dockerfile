FROM python:3.13-alpine

WORKDIR /backend

RUN pip install uv

COPY quizzes/pyproject.toml quizzes/uv.lock /backend/

RUN uv sync --locked

COPY quizzes/app /backend/

CMD ["sh", "-c", "uv run alembic upgrade head && uv run main.py"]
