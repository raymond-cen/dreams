import json
import requests
import pytest
from src import config
from src.error import InputError, AccessError

def test_succeed():
    # Succeed with no messages
    user_info = {
        "email": "vds32152il@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }

    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload = user_register.json()
    user_info = {
        "email": "v4ldjt1212il@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }
    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload2 = user_register.json()
    dm_info = {
        'token': payload['token'],
        'u_ids': [payload2['auth_user_id']]
    }
    dm_id = requests.post(f'{config.url}dm/create/v1', json=dm_info) # change data input
    payload3 = dm_id.json()
    message_params = {
        'token': payload['token'],
        'dm_id': payload3['dm_id'],
        'start': 0
    }
    resp = requests.get(f'{config.url}/dm/messages/v1', params=message_params)
    assert resp.status_code == 200
