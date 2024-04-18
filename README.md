# Real Estate Back

### Create Project
```
django-admin startproject "project_name"
```

<!-- Create App -->
python3 manage.py startapp "app_name"

pip freeze > requirements.txt
pip install -r requirements.txt

<!-- Run -->
python3 manage.py runserver

<!-- Create Admin -->
python3 manage.py migrate
python3 manage.py createsuperuser

<!-- Make Migration -->
python3 manage.py makemigrations
python3 manage.py migrate

<!-- Virtual Env -->
virtualenv env
. env/bin/activate

<!-- collect admin static -->
python3 manage.py collectstatic

source venv/bin/activate