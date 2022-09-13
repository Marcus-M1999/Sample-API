FROM python:3.10 as venv

# Install poetry, see https://python-poetry.org/docs/#installation
ENV POETRY_VERSION=1.2.0
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# Install dependencies
WORKDIR /app

RUN python -m venv /app/lab1
COPY lab1/pyproject.toml ./


ARG POETRY_OPTIONS
RUN . /app/lab1/bin/activate \
    && poetry install $POETRY_OPTIONS

FROM python:3.10 as prod

WORKDIR /app

COPY --from=venv /app/lab1 /app/lab1/

ENV PATH /app/lab1/bin:${PATH}


COPY lab1/src/main.py ./

EXPOSE 8000

#HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000', timeout=2)"

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]