import requests
from django.conf import settings


def check_recaptcha(request_data):
    recaptcha_response = request_data.get('recaptcha', '')
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result['success']
