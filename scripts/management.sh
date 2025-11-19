#!/bin/bash

# Выполнение manage.py команд в контейнере
if [ -z "$1" ]; then
    echo "Usage: ./scripts/management.sh <command>"
    echo "Example: ./scripts/management.sh migrate"
    exit 1
fi

docker-compose exec web python manage.py "$@"