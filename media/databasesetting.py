import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'media',
        'USER': 'root',
        'PASSWORD': 'Spring2017!',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
    'sqllite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}



#This is sqllite - Keeping code in case we want to switch to sql lite in future

"""import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
