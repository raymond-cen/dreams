import json
import requests
import pytest
from src import config

def test_succeed():
    user_info = {
        "email": "h44ch4m4@gmail.com",
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
        'length': 1
    }
    requests.post(f'{config.url}/standup/start/v1', json=data)
    data = {
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi"
    }
    requests.post(f'{config.url}/standup/send/v1', json=data)
    standup_send = requests.post(f'{config.url}/standup/send/v1', json=data)
    assert standup_send.status_code == 200 

def test_inactive_send():
    user_info = {
        "email": "1n4@gmail.com",
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
    requests.post(f'{config.url}/standup/send/v1', json=data)
    standup_send = requests.post(f'{config.url}/standup/send/v1', json=data)
    assert standup_send.status_code == 400