setup_python_env:
	pip install virtualenv
	rm -rf venv
	python3 -m virtualenv venv
	chmod 755 venv/bin/activate
	venv/bin/activate
	pip install -r requirements.txt

start:
	docker-compose up -d

stop:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose up -d --build

restart:
	docker-compose restart

shell:
	docker-compose exec web bash

makemigrations: start
	docker-compose exec web ./manage.py makemigrations

migrate: start
	docker-compose exec web ./manage.py migrate

runcrons: start
	docker-compose exec web ./manage.py crontab add

showcrons: start
	docker-compose exec web ./manage.py crontab show

test: start
	docker-compose exec web ./manage.py test

loaddata: start
	docker-compose exec web ./manage.py loaddata todo/fixtures/* || true

logs:
	docker-compose logs -f web


dummy_data: start
	docker-compose exec web ./manage.py dumpdata todo auth.user authtoken.token  > todo/fixtures/dummy_data.json
