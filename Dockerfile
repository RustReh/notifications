FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["python", "-m", "src.main"]