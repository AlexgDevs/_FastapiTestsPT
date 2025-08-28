FROM python:3.13

WORKDIR /server

RUN pip install poetry

COPY pyproject.toml poetry.lock* .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8000"]