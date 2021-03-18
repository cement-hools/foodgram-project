run:
	docker-compose up --build -d
migrate:
	docker-compose exec web python manage.py migrate --no-input
load_data:
	docker-compose exec web python manage.py loaddata fixtures.json
superuser:
    docker-compose exec web python manage.py createsuperuser
pull:
	docker pull cementhools/foodgram