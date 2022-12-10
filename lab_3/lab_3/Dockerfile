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

RUN python -m venv /app/lab_3
COPY lab_3/pyproject.toml ./


ARG POETRY_OPTIONS
RUN . /app/lab_3/bin/activate \
    && poetry install $POETRY_OPTIONS

FROM python:3.10-slim-buster as prod

WORKDIR /app

COPY --from=venv /app/lab_3 /app/lab_3/

ENV PATH /app/lab_3/bin:${PATH}


COPY lab_3/ ./


EXPOSE 8000

#HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]