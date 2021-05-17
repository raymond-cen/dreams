import json
import requests
import pytest
from src.other import clear_v1
from src import config

def test_logout_succeed():
    user_info = {
        'email' : "vmmlidemail@gmail.com",
        'password' : "123456",
        'name_first' : "ab",
        'name_last' : "cd",
    }
    user_register = requests.post(f'{config.url}auth/register/v2', json = user_info)
    payload = user_register.json()
    logged_out = requests.post(f'{config.url}auth/logout/v1', json = {'token': payload['token']})
    assert logged_out.status_code == 200

def test_invalid_token():
    assert requests.post(f'{config.url}auth/logout/v1', json = {"token": "invalidtoken"}).status_code == 403
