FROM python:3.10

WORKDIR /pizza-delivery-api/pizza-api

COPY ./pizza-api /pizza-delivery-api

COPY ./pizza-api/pyproject.toml /pizza-delivery-api/pyproject.toml

RUN pip3 install poetry

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "pizza-api.pizza_api.entrypoint.app:app", "--reload" ,"--host", "0.0.0.0", "--port", "8000"]
