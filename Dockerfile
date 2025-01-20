FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y locales-all

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/app/src

RUN pip install uv

COPY ./pyproject.toml pyproject.toml

RUN uv sync

COPY . .

CMD ["python"]