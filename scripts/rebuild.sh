#!/bin/bash

# Пересборка и перезапуск сервисов
echo "Rebuilding Habit Tracker services..."

docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "Services rebuilt and restarted."