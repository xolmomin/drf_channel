mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

create_admin:
	./manage.py createsuperuser --username admin --email admin@mail.ru