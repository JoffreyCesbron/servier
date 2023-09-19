FROM python:3.9-slim-buster

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["python", "src/pipeline/main.py"]
