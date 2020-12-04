import os

import requests


port = os.environ.get('BACK_END_PORT')
api_url = f'http://back-end:{port}/api/tgbot/'

def check_user(chat_id):
    params = {'chat_id': chat_id}
    response = requests.get(api_url + 'session/', params=params)
    # Check if user exists (response.json() returns a list)
    return bool(response.json())

def get_user_name(chat_id):
    return 'Иванов Иван Иванович'

def get_user_milgroup(chat_id):
    return '1809'

def reset_user(chat_id):
    return True

def try_to_auth(chat_id, code):
    params = {'code': code}
    response = requests.get(api_url + 'session/', params=params)
    # Check if code exists
    data = response.json()
    if not data:
        return False
    # Check if code is used
    session = data[0]
    if session['chat_id'] is not None:
        return False
    patch_data = {'chat_id': chat_id}
    response = requests.patch(api_url + f'session/{session["id"]}/',
                                data=patch_data)
    return response.status_code // 100 == 2
