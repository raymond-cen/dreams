import json
import requests
import pytest
from src import config
from src.error import InputError, AccessError

def test_succeed():
    # Succeed with no messages
    user_info = {
        "email": "validemail@gmail.com",
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

    message_params = {
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'start': 0
    }
    resp = requests.get(f'{config.url}channel/messages/v2', params=message_params)
    assert resp.status_code == 200

def test_invalid_start():
    user_info = {
        "email": "valide12mail@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }

    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload = user_register.json()
    channel_info = {
        'token': payload['token'],
        'name': "channel2",
        'is_public': True
    }
    channel_id = requests.post(f'{config.url}channels/create/v2', json=channel_info) # change data input
    payload2 = channel_id.json()

    message_params = {
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'start': 340
    }
    resp = requests.get(f'{config.url}channel/messages/v2', params=message_params)
    assert resp.status_code == 400
