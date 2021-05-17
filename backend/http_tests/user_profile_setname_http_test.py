import requests
import json
from src import config
from src.auth import create_token

def test_setname_success():
    user_info = {"email": "abcd@gmil.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    global user
    user = requests.post(config.url + 'auth/register/v2', json = user_info)    
    global user_dict
    user_dict = user.json()
    payload = {"token" : user_dict['token'], 'name_first': "aabb", 'name_last': "bb"}
    result = requests.put(config.url + 'user/profile/setname/v2', json = payload)
    assert result.status_code == 200     

def test_setname_no_first_name():
    payload = {'token': user_dict['token'], 'name_first': "", 'name_last': "c"}
    assert requests.put(config.url + 'user/profile/setname/v2', json = payload).status_code == 400    
      
def test_setname_long_first_name():
    payload = {'token': user_dict['token'], 'name_first': "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu", 'name_last': "c"}
    assert requests.put(config.url + 'user/profile/setname/v2', json = payload).status_code == 400 
    
def test_setname_no_last_name():
    payload = {'token': user_dict['token'], 'name_first': "a", 'name_last': ""}
    assert requests.put(config.url + 'user/profile/setname/v2', json = payload).status_code == 400    
   
def test_setname_long_last_name():
    payload = {'token': user_dict['token'], 'name_first': "a", 'name_last': "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu"}
    assert requests.put(config.url + 'user/profile/setname/v2', json = payload).status_code == 400    
       
def test_setname_invalid_token():
    bad_token = create_token(-5, 1)
    payload = {'token': bad_token, 'name_first': "q", 'name_last': "w"}
    assert requests.put(config.url + 'user/profile/setname/v2', json = payload).status_code == 403    

