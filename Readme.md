# Frest_django

## Технологии
- Django
- Celery
- Redis

## Запуск

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up -d
   ```
   
2. Приложение будет доступно по адресу: http://localhost:8000

### Итог:
- Ваш текущий `docker-compose.yml` рабочий, но добавление `healthcheck` и уточнение `Readme.md` сделает запуск более надежным и понятным для других разработчиков.