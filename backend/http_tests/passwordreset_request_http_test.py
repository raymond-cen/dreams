import requests
import json
import pytest
from src import config
from src.error import InputError
from src.other import clear_v1

def test_register_existing_email():
    clear_v1()
    user_info = {"email": "raymondcn2005@gmail.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    requests.post(config.url + 'auth/register/v2', json = user_info)    
    user_reset = requests.post(config.url+ '/auth/passwordreset/request/v1', json = {'email': 'raymondcn2005@gmail.com'})
    assert user_reset.status_code == 200

def test_register_no_email():
    user_reset = requests.post(config.url+ '/auth/passwordreset/request/v1', json = {"email": ""})
    assert user_reset.status_code == 500
