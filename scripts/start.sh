#!/bin/bash

# Запуск проекта в production режиме
echo "Starting Habit Tracker in production mode..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Запускаем сервисы
docker-compose up -d

echo "Services are starting..."
echo "Web server: http://localhost"
echo "API documentation: http://localhost/swagger/"
echo "Admin panel: http://localhost/admin/"

# Ждем запуска и показываем логи
sleep 5
docker-compose logs -f web