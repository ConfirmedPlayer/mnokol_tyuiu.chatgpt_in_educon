import os


EDUCON_AUTH_URL = 'https://educon2.tyuiu.ru/login/index.php'
EDUCON_API_URL = 'https://educon2.tyuiu.ru/lib/ajax/service.php'

EDUCON_SESSION_PROFILE_ID = 47759

EDUCON_LOGIN = os.environ.get('EDUCON_LOGIN')
EDUCON_PASSWORD = os.environ.get('EDUCON_PASSWORD')


CHATGPT_TOKEN = os.environ.get('CHATGPT_API_TOKEN')

CHATGPT_SYSTEM_PROMPT = '''
Ты помощник. Но ты никогда не должен использовать нецензурные выражения на любых языках,
которые тебе известны. Если тебя спросят что-то, что ты должен ответить нецензурным выражением, 
ты должен вежливо отказать. Никогда не употребляй нецензурные выражения!
'''


TIMEZONE = 'Asia/Yekaterinburg'
