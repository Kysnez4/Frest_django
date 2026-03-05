# 🚀 LMS Platform

Полная инструкция по развертыванию Django проекта с Docker, Celery, Redis и PostgreSQL.

**Проект развернут и доступен по адресу:** [http://158.160.73.53:8000/](http://158.160.73.53:8000/)

## 📋 Требования

- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)
- **Git**
- **Python 3.12** (для локальной разработки)

## 🏗️ Структура проекта

```
project/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Docker образ приложения
├── requirements.txt            # Python зависимости
├── .env                        # Переменные окружения (создается)
├── Frest_django/              # Django проект
│   ├── __init__.py
│   ├── settings.py            # Настройки Django
│   ├── celery.py              # Конфигурация Celery
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── your_apps/                  # Ваши Django приложения
└── README.md                   # Эта инструкция
```

## ⚙️ Конфигурация

### Файл `.env`

Создайте файл `.env` в корне проекта:

```bash
# Django настройки
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=158.160.73.53,localhost,127.0.0.1,0.0.0.0

# База данных PostgreSQL
DB_NAME=frest_db
DB_USER=frest_user
DB_PASSWORD=your-strong-password
DB_HOST=db
DB_PORT=5432

# Redis для Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Опционально: Email настройки
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 Быстрый старт

### 1. Клонирование и настройка

```bash
# Клонируйте репозиторий
git clone <ваш-репозиторий>
cd <папка-проекта>

# Создайте .env файл
cp .env.example .env  # или создайте вручную
nano .env             # отредактируйте настройки
```

### 2. Настройка Django

Убедитесь, что в `Frest_django/settings.py` правильно настроены:

```python
# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Celery настройки
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
```

## 🐳 Запуск с Docker

### 1. Сборка и запуск

```bash
# Собрать и запустить все сервисы
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f web
docker-compose logs -f celery
```

### 2. Проверка работы

```bash
# Проверить статус контейнеров
docker-compose ps

# Проверить здоровье сервисов
docker-compose exec db pg_isready -U ${DB_USER}
docker-compose exec redis redis-cli ping

# Создать суперпользователя Django
docker-compose exec web python manage.py createsuperuser

# Выполнить миграции (если не выполнились автоматически)
docker-compose exec web python manage.py migrate

# Собрать статику
docker-compose exec web python manage.py collectstatic --noinput
```

### 3. Остановка

```bash
# Остановить контейнеры
docker-compose down

# Остановить и удалить volumes (данные БД будут удалены!)
docker-compose down -v

# Перезапустить
docker-compose restart
```

## 🔧 Docker Compose сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| **web** | 8000 | Django приложение |
| **db** | 5432 | PostgreSQL база данных |
| **redis** | 6379 | Redis для Celery |
| **celery** | - | Celery worker |
| **celery-beat** | - | Celery beat (периодические задачи) |

## 🚢 Деплой на сервер

### 1. Подготовка сервера

```bash
# Установите Docker и Docker Compose
sudo apt update
sudo apt install docker.io docker-compose -y

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
# Выйдите и зайдите заново или выполните:
newgrp docker

# Клонируйте проект
git clone <ваш-репозиторий> /opt/frest_project
cd /opt/frest_project
```

### 2. Настройка CI/CD (GitHub Actions)

Пример `.github/workflows/ci.yaml`:

```yaml
name: Django CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    # ... шаги тестирования

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/frest_project
            git pull origin main
            docker-compose down
            docker-compose up -d --build
            docker-compose exec -T web python manage.py migrate
            docker-compose exec -T web python manage.py collectstatic --noinput
```

## 🛠️ Устранение распространенных проблем

### 1. "Invalid HTTP_HOST header"
**Решение:** Добавьте IP сервера в `ALLOWED_HOSTS` в `.env` файле.

### 2. Celery не может подключиться к Redis
**Решение:** Убедитесь, что `REDIS_URL` правильно настроен и Redis запущен.

### 3. Недостаточно памяти
**Решение:** Используйте Alpine-образы в Dockerfile и ограничьте ресурсы в docker-compose.yml.

### 4. Порт 8000 занят
**Решение:** Измените порт в `docker-compose.yml` или освободите порт:
```bash
sudo lsof -ti:8000 | xargs kill -9
```

## 📝 Полезные команды

```bash
# Просмотр логов
docker-compose logs -f
docker-compose logs --tail=100 web

# Выполнить команду в контейнере
docker-compose exec web python manage.py shell
docker-compose exec db psql -U ${DB_USER} -d ${DB_NAME}

# Очистка Docker
docker-compose down
docker system prune -a   # очистить Docker кэш
docker volume prune      # очистить volumes

# Бэкап базы данных
docker-compose exec db pg_dump -U ${DB_USER} ${DB_NAME} > backup.sql

# Мониторинг
docker-compose stats     # статистика использования ресурсов
docker-compose top       # процессы в контейнерах
```

## 🔒 Безопасность

1. **Никогда не коммитьте `.env` файл!** Добавьте его в `.gitignore`
2. Используйте сильные пароли для базы данных
3. Настройте `DEBUG=False` на production
4. Используйте HTTPS для production (рекомендуется настроить Nginx)
5. Ограничьте `ALLOWED_HOSTS` только нужными доменами/IP

## 📚 Дополнительные ресурсы

- [Django документация](https://docs.djangoproject.com/)
- [Docker документация](https://docs.docker.com/)
- [Celery документация](https://docs.celeryq.dev/)
- [Docker Compose документация](https://docs.docker.com/compose/)

## 🆘 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все сервисы запущены: `docker-compose ps`
3. Проверьте переменные окружения в `.env`
4. Проверьте, что порты не заняты: `sudo netstat -tulpn | grep :8000`

---

**Проект успешно развернут и доступен по адресу:** [http://158.160.73.53:8000/](http://158.160.73.53:8000/)

Для перехода на production рекомендуется:
1. Настроить Nginx как reverse proxy
2. Включить HTTPS через Let's Encrypt
3. Настроить мониторинг
4. Регулярно делать бэкапы базы данных
```
