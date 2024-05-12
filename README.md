# Real Estate Back

### Create Project
```
django-admin startproject "project_name"
```

### Create App 
```
python3 manage.py startapp "app_name"
```
```
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Run 
```
python3 manage.py runserver
```

### Create Admin 
```
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Make Migration 
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Virtual Env 
```
virtualenv env
. env/bin/activate
source venv/bin/activate

python -m virtualenv venv
venv\Scripts\activate
```

### Collect Admin Static 
```
python3 manage.py collectstatic
```
