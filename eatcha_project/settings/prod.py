from .commons import *
import os

ALLOWED_HOSTS = "*"
DEBUG = False

import pymysql
pymysql.install_as_MySQLdb()

DEBUG = False
#ORM에서 쿼리 내역이 계속 쌓인다. 그런데 배포환경에서는 서버가 재시작하지 않아서 메모리 가득찬 후에 에러난다.
#예외내역 user에게 노출


#원래는 여기에 사용할 db 설정을 해주어야 한다.
DATABASES = {
 'default': {
     'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
     'HOST': os.environ['DB_HOST'],
     'USER': os.environ['DB_USER'],
     'PASSWORD': os.environ['DB_PASSWORD'],
     'NAME': os.environ['DB_NAME'],
     'PORT': os.environ['DB_PORT'],
 },
}

# 프로젝트.settings.prod_aws_eb
import os

INSTALLED_APPS += ['storages'] # django-storages 앱 의존성 추가

# 기본 static/media 저장소를 django-storages로 변경
STATICFILES_STORAGE = 'eatcha_project.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'eatcha_project.storages.MediaS3Boto3Storage'

# S3 파일 관리에 필요한 최소 설정
# 소스코드에 설정정보를 남기지마세요. 환경변수를 통한 설정 추천
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] # 필수 지정
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] # 필수 지정
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME'] # 필수 지정

AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-northeast-2')
