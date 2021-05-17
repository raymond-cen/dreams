import requests
import json
from src import config
from src.auth import create_token

def test_sethandle_success():
    user_info = {"email": "abcd@gmai.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    global user
    user = requests.post(config.url + 'auth/register/v2', json = user_info)    
    global user_dict
    user_dict = user.json()
    payload = {"token" : user_dict['token'], 'handle_str': "aabbbb"}
    result = requests.put(config.url + 'user/profile/sethandle/v1', json = payload)
    assert result.status_code == 200

def test_sethandle_less_handle():
    payload = {'token': user_dict['token'], 'handle_str': "aa"}
    assert requests.put(config.url + 'user/profile/sethandle/v1', json = payload).status_code == 400    
      
def test_sethandle_long_handle():
    payload = {'token': user_dict['token'], 'handle_str': "shhusensiheuiauhieyde"}
    assert requests.put(config.url + 'user/profile/sethandle/v1', json = payload).status_code == 400 

def test_sethandle_existed_for_another_user():
    user_info = {"email": "aaba@gmai.com", "password": "1234576","name_first": "aa", "name_last": "aa"}
    requests.post(config.url + 'auth/register/v2', json = user_info)   
    payload = {'token': user_dict['token'], 'handle_str': "aaaa"}
    assert requests.put(config.url + 'user/profile/sethandle/v1', json = payload).status_code == 400 

def test_sethandle_invalid_token():
    bad_token = create_token(-5, 1)
    payload = {'token': bad_token, 'handle_str': "bad"}
    assert requests.put(config.url + 'user/profile/sethandle/v1', json = payload).status_code == 403    