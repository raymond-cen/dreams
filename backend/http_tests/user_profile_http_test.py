import requests
import json
from src import config
from src.auth import create_token
from src.data import data

def test_success(): 
    global user 
    user_info = {"email": "dds@gmail.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    user = requests.post(config.url + 'auth/register/v2', json = user_info)
    global user_dict
    user_dict = user.json() 
   
    params = {'token': user_dict['token'], 'u_id': user_dict['auth_user_id']}
    result = requests.get(config.url + 'user/profile/v2', params = params)
    assert  result.status_code == 200 

def test_invalid_user():
    params = {'token': user_dict['token'], 'u_id': -1}
    assert requests.get(config.url + 'user/profile/v2', params = params).status_code == 400

def test_profile_invalid_token():
    bad_token = create_token(-1, 1)
    params = {'token': bad_token, 'u_id': user_dict['auth_user_id']}
    assert requests.get(config.url + 'user/profile/v2', params = params).status_code == 403   
