import json
import requests
import pytest
from src import config

def test_succeed():
    user_info = {
        "email": "p3k0r4@gmail.com",
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
    message = message.json()

    data = {
        'token': payload['token'],
        'query_str': 'h'
    }
    message_react = requests.get(f'{config.url}/search/v2', params=data)
    assert message_react.status_code == 200 
