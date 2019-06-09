.PHONY: db runserver makemigrations shell daphne

db:
	docker volume create --name hacking_carrots_pg_data
	docker run --name carrot-db --rm -d -p '5432:5432' -v 'hacking_carrots_pg_data:/var/lib/postgresql/data' -e 'POSTGRES_DB=carrot' -e 'POSTGRES_USER=carrot' -e 'POSTGRES_PASSWORD=carrot' postgres
	docker run --name carrot-redis --rm -d -p '6379:6379' redis

runserver:
	DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run python src/manage.py migrate
	@DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run python src/manage.py runserver


makemigrations:
	cd src
	DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run python src/manage.py makemigrations

shell:
	cd src
	@DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run python src/manage.py shell

daphne:
	cd src && DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run daphne -b 0.0.0.0 -p 8000 --access-log=- -v 2 carrots.asgi:application

cmd:
	cd src && DATABASE_URL=postgres://carrot:carrot@0.0.0.0:5432/carrot REDIS_HOST=0.0.0.0 pipenv run python manage.py createsuperuser
