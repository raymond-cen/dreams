import requests
import json
from src import config
from src.auth import create_token

def test_setname_success():
    user_info = {"email": "abcd@gmal.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    global user
    user = requests.post(config.url + 'auth/register/v2', json = user_info)    
    global user_dict
    user_dict = user.json()
    payload = {"token" : user_dict['token'], "email": "aabba@gmail.com"}
    result = requests.put(config.url + 'user/profile/setemail/v2', json = payload)
    assert result.status_code == 200

def test_setemail_invalid_email():
    payload = {'token': user_dict['token'], 'email': "bad.com"}
    assert requests.put(config.url + 'user/profile/setemail/v2', json = payload).status_code == 400    
      
def test_setemail_existed_for_another_user():
    user_info = {"email": "aaa@mail.com", "password": "1234576","name_first": "abc", "name_last": "c"}
    requests.post(config.url + 'auth/register/v2', json = user_info)    
    payload = {'token': user_dict['token'], 'email': "aaa@mail.com"}
    assert requests.put(config.url + 'user/profile/setemail/v2', json = payload).status_code == 400 

def test_setemail_invalid_token():
    bad_token = create_token(-5, 1)
    payload = {'token': bad_token, 'email': "ava@gmail.com"}
    assert requests.put(config.url + 'user/profile/setemail/v2', json = payload).status_code == 403    