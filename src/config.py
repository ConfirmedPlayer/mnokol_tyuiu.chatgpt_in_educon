import os


EDUCON_AUTH_URL = 'https://educon2.tyuiu.ru/login/index.php'
EDUCON_API_URL = 'https://educon2.tyuiu.ru/lib/ajax/service.php'

EDUCON_SESSION_PROFILE_ID = 47759

EDUCON_LOGIN = os.environ.get('EDUCON_LOGIN', 'lagutkinvd@std.tyuiu.ru')
EDUCON_PASSWORD = os.environ.get('EDUCON_PASSWORD', 'Temnomor.ru!0')


CHATGPT_TOKEN = os.environ.get('CHATGPT_API_TOKEN', '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')


TIMEZONE = 'Asia/Yekaterinburg'
