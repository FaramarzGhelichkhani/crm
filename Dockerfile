FROM python:3.8.5

WORKDIR /app

RUN pip --no-cache-dir install  poetry && \
    rm -rf app/.cache/pip

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \ 
    poetry install --no-interaction --no-ansi --no-cache

COPY . /app
