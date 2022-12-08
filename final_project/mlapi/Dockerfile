FROM python:3.10-slim-buster as venv

RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry, see https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.2.0
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# Install dependencies
WORKDIR /app

RUN python -m venv /app/mlapi
COPY mlapi/pyproject.toml ./


ARG POETRY_OPTIONS
RUN . /app/mlapi/bin/activate \
    && poetry install $POETRY_OPTIONS

FROM python:3.10-slim-buster as prod

WORKDIR /app

COPY --from=venv /app/mlapi /app/mlapi/

ENV PATH /app/mlapi/bin:${PATH}


COPY mlapi/ ./


EXPOSE 8000

#HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]