import requests
import json
from src import config
from src.auth import create_token

def test_users_all_success():  
    user_info = {"email": "abcd@gml.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    user = requests.post(config.url + 'auth/register/v2', json = user_info)    
    user_dict = user.json()
    print(user_dict) 
    params = {'token': user_dict['token']}
    ret = requests.get(config.url + 'users/all/v1', params = params)
    print(ret.json())
    assert ret.status_code == 200


def test_users_all_invalid_token():
    bad_token = create_token(-5, 1)
    params = {'token': bad_token}
    assert requests.get(config.url + 'users/all/v1', params = params).status_code == 403   