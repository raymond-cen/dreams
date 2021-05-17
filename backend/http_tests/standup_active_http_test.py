import json
import requests
import pytest
from src import config

def test_succeed():
    user_info = {
        "email": "4y4m3@gmail.com",
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
    }
    standup_send = requests.get(f'{config.url}/standup/active/v1', params=data)
    assert standup_send.status_code == 200 

def test_inactive_send():
    user_info = {
        "email": "rush14@gmail.com",
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
        'channel_id': payload2['channel_id'] + 3213,
    }
    standup_send = requests.get(f'{config.url}/standup/active/v1', params=data)
    assert standup_send.status_code == 400