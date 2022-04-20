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
	docker-compose run web bash

makemigrations: start
	docker-compose run web ./manage.py makemigrations

migrate: start
	docker-compose run web ./manage.py migrate

runcrons: start
	docker-compose run web ./manage.py crontab add

showcrons: start
	docker-compose run web ./manage.py crontab show

test: start
	docker-compose run web ./manage.py test

loaddata: start
	docker-compose run web ./manage.py loaddata todo/fixtures/* || true

logs:
	docker-compose logs -f web


dummy_data: start
	docker-compose run web ./manage.py dumpdata todo auth.user authtoken.token  > todo/fixtures/dummy_data.json



coverage:
	docker-compose run web coverage run --source='.' manage.py test todo
	docker-compose run web coverage report

attach_mode: start
	docker attach drf-todo_web_1
