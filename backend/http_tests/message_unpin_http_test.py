import json
import requests
import pytest
from src import config

def test_succeed():
    user_info = {
        "email": "k0r0n3@gmail.com",
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
        'message_id': message['message_id']
    }
    requests.post(f'{config.url}/message/pin/v1', json=data)
    message_pin = requests.post(f'{config.url}/message/unpin/v1', json=data)
    assert message_pin.status_code == 200 

def test_already_pinned():
    user_info = {
        "email": "copiumaf@gmail.com",
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
        'message_id': message['message_id']
    }

    message_pin = requests.post(f'{config.url}/message/unpin/v1', json=data)
    assert message_pin.status_code == 400