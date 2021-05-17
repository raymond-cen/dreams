import json
import requests
import pytest
from src import config
from src.error import InputError

def test_login_succeed():
    user_info = {
        'email' : "nicevalidmail2@gmail.com",
        'password' : "123456",
        'name_first' : "ab",  
        'name_last' : "cd",
    }
    requests.post(f'{config.url}auth/register/v2', json = user_info)
    user_login = requests.post(f'{config.url}auth/login/v2', json = {'email': "nicevalidmail2@gmail.com", 'password': "123456"})
    assert user_login.status_code == 200

def test_non_existing_email():
    user_login = {'email': "emaildoesnot@gmail.com", 'password': "123456"}
    resp = requests.post(config.url+ 'auth/login/v2', json=user_login)
    assert resp.status_code == 400

def test_invalid_email():
    user_login = {'email': "invalidemail.com", 'password': "123456"}
    resp = requests.post(config.url+ 'auth/login/v2', json=user_login)
    assert resp.status_code == 400

def test_empty_arguments():
    user_login = {'email': "", 'password': ""}
    resp = requests.post(config.url+ 'auth/login/v2', json=user_login)
    assert resp.status_code == 400

def test_wrong_password():
    user_login = {'email': "validemail@gmail.com", 'password': "wrongpassword"}
    resp = requests.post(config.url+ 'auth/login/v2', json=user_login)
    assert resp.status_code == 400

def test_blank_password():
    user_login = {'email': "validemail@gmail.com", 'password': ""}
    resp = requests.post(config.url+ 'auth/login/v2', json=user_login)
    assert resp.status_code == 400
