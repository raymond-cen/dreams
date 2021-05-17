import json
import requests
import pytest
from src import config
from src.error import InputError, AccessError

def test_valid_edit():
    user_info = {
        "email": "validemailvxc@gmail.com",
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
    data2 = {
        'token': payload['token'],
        'message_id': message['message_id'],
        'message': "editedmessage"
    }
    message = requests.put(f'{config.url}message/edit/v2', json=data2)
    assert message.json() == {}

def test_invalid_auth():
    user_info = {
        "email": "validemailvxcd@gmail.com",
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
    data2 = {
        'token': payload['token'] + "invalidddsdtoken",
        'message_id': message['message_id'],
        'message': "editedmessage"
    }
    message = requests.put(f'{config.url}message/edit/v2', json=data2)
    assert message.status_code == 400
