from buskoin.settings.settings import *

DEBUG=False

ALLOWED_HOSTS = [
    '128.199.184.32',
	'localhost',
	'api.buskoin.com',
	'buskoin.com',
]

BASE_API_URL = "https://api.buskoin.com"

CORS_ALLOWED_ORIGINS = [
    "https://buskoin.com",
    "https://www.buskoin.com",
]