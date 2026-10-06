
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EXAMPLE-SK:a&mn@2#h6)f1dqrko#37=o-@4&r#a$nd1fqah!!#kuj!odfz&8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'domain.com'
]

EMAIL_SETTINGS = {
        'EMAIL_HOST': 'mail.domain.com',
        'EMAIL_PORT': '465',
        'EMAIL_HOST_USER': 'correo@domain.com',
        'EMAIL_HOST_PASSWORD': 'password',
        'EMAIL_USE_SSL': True,
        'DEFAULT_FROM_EMAIL': 'Sistemas IMGX<no-reply@imagilex.com.mx>',
    }


def DATABASES(os, BASE_DIR):
    # db = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'managed/managed.imgx'),
    #     }
    # }
    db = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'host',
            'PORT': '3306',
            'OPTIONS': {
                'read_default_file': 'managed/managed_db.imgx',
                'init_command': 'SET default_storage_engine=INNODB',
                'autocommit': True,
            },
        },
        'app_reports': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'host',
            'PORT': '3306',
            'OPTIONS': {
                'read_default_file': 'managed/managed_db_2.imgx',
                'init_command': 'SET default_storage_engine=INNODB',
                'autocommit': True,
                # 'sql_mode': 'STRICT_TRANS_TABLES',
            },
            'NAME': 'database',
            'USER': 'user',
            'PASSWORD': 'password',
        }
    }
    return db

STATIC_URL = '/static/'
STATIC_ROOT = '/home/usuario/dominio.com/public_html/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/usuario/dominio.com/public_html/media/'
