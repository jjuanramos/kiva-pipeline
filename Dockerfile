FROM python:3.8.5-slim AS base

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="$PATH:/runtime/bin" \
  PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.8/site-packages" \
  # Versions:
  POETRY_VERSION=1.1.5

# System deps:
RUN apt-get update && apt-get install -y build-essential unzip wget python-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY pyproject.toml poetry.lock /src/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

COPY . /src

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY . /app
WORKDIR /app
EXPOSE 80
CMD ["uvicorn", "kiva_pipeline.app:app", "--host", "0.0.0.0", "--port", "80"]

# docker build . --tag kiva_pipeline
# docker run --name kiva_pipeline_container -p 80:80 kiva_pipeline