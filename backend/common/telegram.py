import requests
from WebAdmin.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_tg_message(message):
    r = requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
                      json={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
    return r.status_code == 200
