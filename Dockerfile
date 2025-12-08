FROM python:3.12-slim

WORKDIR /code

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock* /code/

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем проект
COPY . /code/

# Создаем статическую папку
RUN mkdir -p /code/static

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]