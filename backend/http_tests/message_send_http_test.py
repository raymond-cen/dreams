import json
import requests
import pytest
from src import config
from src.error import InputError, AccessError

def test_succeed():
    user_info = {
        "email": "valide212il@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }

    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload = user_register.json()
    channel_info = {
        'token': payload['token'],
        'name': "channel1",
        'is_public': True
    }
    channel_id = requests.post(f'{config.url}channels/create/v2', json=channel_info) # change data input
    payload2 = channel_id.json()
    data = {
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi"
    }
    message = requests.post(f'{config.url}/message/send/v2', json=data)

    assert message.status_code == 200 

def test_non_auth_user():
    # over 1000 characters long message
    user_info = {
        "email": "validemail22@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }

    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload = user_register.json()

    channel_info = {
        'token': payload['token'],
        'name': "channel1",
        'is_public': True
    }
    channel2= requests.post(f'{config.url}channels/create/v2', json=channel_info) # change data input
    payload2 = channel2.json()

    user_login = {'email': "valide21fxg2@gmail.com", 'password': "123456", "name_first": 'vd', "name_last": 'sada'}
    resp = requests.post(f'{config.url}auth/register/v2', json=user_login)
    resp = resp.json()
    print(resp)
    data = {
        'token': resp['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi"
    }

    message = requests.post(f'{config.url}/message/send/v2', json=data)
    assert message.status_code == 403
