MANAGE := poetry run python manage.py

setup: install makemigrations migrate

install:
	poetry install

makemigrations:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

dev:
	python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) sina_site.wsgi:application

lint:
	poetry run flake8 sina_site

test:
	@$(MANAGE) test

test-coverage:
	poetry run pytest --cov=sina_site --cov-report xml

compil:
	python manage.py compilemessages