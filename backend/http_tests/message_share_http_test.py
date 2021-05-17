import json
import requests
import pytest
from src import config
from src.error import InputError, AccessError

def test_valid_send():

    user_info = {
        "email": "valide654mail@gmail.com",
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
        'og_message_id': message['message_id'],
        'channel_id': payload2['channel_id'],
        'dm_id': -1,
        'message': "hi"
    }
    shared_message = requests.post(f'{config.url}/message/share/v1', json=data)
    assert shared_message.status_code == 200
