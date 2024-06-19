MANAGE := poetry run python manage.py

setup: install makemigrations migrate createsuperuser

install:
	poetry install

makemigrations:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

createsuperuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$(USERNAME_SUPERUSER)').exists() or User.objects.create_superuser('$(USERNAME_SUPERUSER)', 'admin@example.com', '$(PASSWORD_SUPERUSER)')" | $(MANAGE) shell

dev:
	python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) --timeout 60 sina_site.wsgi:application

lint:
	poetry run flake8 sina_site

test:
	@$(MANAGE) test

test-coverage:
	poetry run pytest --cov=sina_site --cov-report xml

compil:
	python manage.py compilemessages