FROM python:3.10

WORKDIR /app

COPY ./pizza-api ./app

RUN pip install poetry

COPY ./pizza-api/poetry.lock ./poetry.lock

COPY ./pizza-api/pyproject.toml ./pyproject.toml

RUN poetry config virtualenvs.create false

RUN poetry install

ENTRYPOINT ["uvicorn", "pizza-delivery-api.pizza-api.pizza_api.entrypoint.app:app", "--host", "0.0.0.0", "--port", "8000"]
