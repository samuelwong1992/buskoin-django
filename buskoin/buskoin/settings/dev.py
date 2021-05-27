from buskoin.settings.settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

IS_DEV = True
BASE_API_URL = "http://127.0.0.1:8001"
BASE_URL = "http://127.0.0.1:8080/#/"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://192.168.1.112:8080",
]