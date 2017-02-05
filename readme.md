# Local run

To run the project locally:

* clone repo
* `cd employees/`  
* `virtualenv venv`
* `source venv/bin/activate`  
* `pip install -r requirements.txt`  
* create file `employees/local_settings.py` and fill like in example below   
* create database, user, grant perms to user  
* run migrations `./manage.py migrate` 
* create superuser `./manage.py createsuperuser`
* run dev server `./manage.py runserver`

**Development local_settings.py example**

    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dbname',
            'USER': 'dbuser',
            'PASSWORD': 'dbpassword',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

