ARG PYTHON_IMAGE=python:3.12-slim-bookworm
FROM $PYTHON_IMAGE as build

ARG PYTHON_UV_VERSION=>=0.4.4

ARG NEXUS_USERNAME
ARG NEXUS_PASSWORD

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

RUN pip install uv
RUN uv venv /app/.venv
COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --no-cache
FROM $PYTHON_IMAGE
RUN apt-get update -y && apt-get install -y media-types
RUN addgroup --gid 2000 app && adduser --gid 2000 --uid 1000 app
USER app

WORKDIR /app
ENV PYTHONPATH=$PYTHONPATH:/app/src \
    PATH=/app/.venv/bin:$PATH \
    PYTHONUNBUFFERED=1

COPY --from=build --chown=app:app /app/.venv /app/.venv
COPY ./src ./src
COPY ./alembic ./alembic
COPY alembic.ini ./

CMD ["sh","-c","alembic upgrade head && uvicorn src.server:create_app --factory --loop uvloop --host 0.0.0.0"]
