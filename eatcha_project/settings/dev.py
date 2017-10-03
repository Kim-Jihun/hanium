from .commons import *

#DJANGO DEGUB TOOLBAR 설치
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']


DEBUG = True
# midify
ALLOWED_HOSTS = ["*"] # 서비스 주소


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
