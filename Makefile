.PHONY: help build up down logs restart rebuild test clean

help:
	@echo "Available commands:"
	@echo "  make build     - Build the containers"
	@echo "  make up        - Start the containers"
	@echo "  make down      - Stop the containers"
	@echo "  make logs      - Show container logs"
	@echo "  make restart   - Restart the containers"
	@echo "  make rebuild   - Rebuild the containers"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Remove all containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

clean:
	docker-compose down -v
	docker system prune -f

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

shell:
	docker-compose exec web python manage.py shell

celery-logs:
	docker-compose logs -f celery

beat-logs:
	docker-compose logs -f celery-beat

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f