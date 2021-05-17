import json
import requests
import pytest
from src import config
from src.auth import create_token


def test_succeed():
    requests.delete(f'{config.url}clear/v1')
    user_info = {
        "email": "dsat132dsa@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }
    user_info2 = {
        "email": "vdsaevq2@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }
    user_register1 = requests.post(f'{config.url}auth/register/v2', json = user_info)
    user_register2 = requests.post(f'{config.url}auth/register/v2', json = user_info2)
    payload1 = user_register1.json()
    payload2 = user_register2.json()
    payload = {
        'token': payload1['token'],
        'u_id': payload2['auth_user_id']
    }

    resp = requests.delete(f'{config.url}admin/user/remove/v1', json = payload)

    assert resp.status_code == 200

def test_onlyowner():
    user_info = {
        "email": "uhafiu532s@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }

    user_register1 = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload1 = user_register1.json()
    payload = {
        'token': create_token(1, 213),
        'u_id': [payload1['auth_user_id']]
    }
    resp = requests.delete(f'{config.url}admin/user/remove/v1', json = payload)
    print(resp.json())
    assert resp.status_code == 400

def test_invalid_auth():
    user_info = {
        "email": "u1233ss@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }
    user_info2 = {
        "email": "uh421ss2@gmail.com",
        "password": "123456",
        "name_first": "ab", 
        "name_last": "cd"
        }
    user_register1 = requests.post(f'{config.url}auth/register/v2', json = user_info)
    user_register2 = requests.post(f'{config.url}auth/register/v2', json = user_info2)
    payload1 = user_register1.json()
    payload2 = user_register2.json()
    payload = {
        'token': payload2['token'],
        'u_id': payload1['auth_user_id']
    }

    resp = requests.delete(f'{config.url}admin/user/remove/v1', json = payload)

    assert resp.status_code == 403
