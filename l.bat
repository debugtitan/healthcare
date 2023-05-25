cls
python manage.py makemigrations frontend
python manage.py migrate frontend
python manage.py makemigrations blogPage
python manage.py migrate blogPage
python manage.py makemigrations adminpage
python manage.py migrate adminpage
python manage.py migrate
python manage.py collectstatic
git add .
git commit -m "new updates forwarded"
git push