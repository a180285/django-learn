django-admin startproject mysite
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
sudo python manage.py runserver 0.0.0.0:80
nohup python manage.py runserver 127.0.0.1:8000 2>&1 1>log &
./manage.py collectstatic -v0 --noinput

python manage.py startapp polls

python manage.py migrate
python manage.py makemigrations polls
python manage.py shell
python manage.py createsuperuser

python manage.py test polls

python -c "import django; print(django.__path__)"

