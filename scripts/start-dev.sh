#!/bin/bash

# Запуск проекта в development режиме
echo "Starting Habit Tracker in development mode..."

# Создаем .env файл для разработки если его нет
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Запускаем сервисы
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

echo "Development services are starting..."
echo "Django development server: http://localhost:8000"
echo "API documentation: http://localhost:8000/swagger/"
echo "Admin panel: http://localhost:8000/admin/"

# Показываем логи
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f web