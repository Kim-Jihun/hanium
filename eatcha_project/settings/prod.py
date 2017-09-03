from .commons import *


ALLOWED_HOSTS = ['사용하는 url']

DEBUG = False
#ORM에서 쿼리 내역이 계속 쌓인다. 그런데 배포환경에서는 서버가 재시작하지 않아서 메모리 가득찬 후에 에러난다.
#예외내역 user에게 노출


#원래는 여기에 사용할 db 설정을 해주어야 한다.
#DATABASES = {
# 'default': {
# 'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'), # ENGINE
# 'HOST': os.environ.get('DATABASE_HOST', None), # 데이터베이스_호스트
# 'NAME': os.environ.get('DATABASE_NAME', None), # 데이터베이스_DB명
# 'USER': os.environ.get('DATABASE_USER', None), # 데이터베이스_유저
# 'PASSWORD': os.environ.get('DATABASE_PASSWORD', None), # 데이터베이스_암호
# },
#}
