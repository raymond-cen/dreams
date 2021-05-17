import requests
import json
import pytest
from src import config
from src.error import InputError

def test_register_valid():
    user_info = {"email": "abcd@gmail.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    user_reg = requests.post(config.url + 'auth/register/v2', json = user_info)    
    requests.post(config.url+ 'auth/login/v2', json = {"email": "abcd@gmail.com", "password": "123456"})
    assert user_reg.status_code == 200

def test_register_whitespace_first_name():
    user_info = {"email": "aa.k@ak.com", "password": "102acd", "name_first": "a ", "name_last": "cd"}
    user_reg = requests.post(config.url + 'auth/register/v2', json = user_info)    
    reg_dict = user_reg.json()
    user_log = requests.post(config.url+ 'auth/login/v2', json = {"email": "aa.k@ak.com", "password": "102acd"})
    log_dict = user_log.json()
    assert reg_dict['auth_user_id'] == log_dict['auth_user_id']

# def test_register_at_last_name():
#     # Test for '@' first name
#     user_info = {"email": "jw.k@kr.com", "password": "102acd", "name_first": "jw", "name_last": "ki@"}
#     user_reg = requests.post(config.url + 'auth/register/v2', json = user_info)    
#     reg_dict = user_reg.json()
#     user_log = requests.post(config.url+ 'auth/login/v2', json = {"email": "jw.k@kr.com", "password": "102acd"})
#     log_dict = user_log.json()
#     assert reg_dict['auth_user_id'] == log_dict['auth_user_id']

# def test_long_handle():
#     user_info = {"email": "kjw.k@kr.com", "password": "102acd", "name_first": "jjwwhiosoensov", "name_last": "kikimheiosonv"}
#     user_reg = requests.post(config.url + 'auth/register/v2', json = user_info)    
#     reg_dict = user_reg.json()
#     user_log = requests.post(config.url+ 'auth/login/v2', json = {"email": "kjw.k@kr.com", "password": "102acd"})
#     log_dict = user_log.json()
#     assert reg_dict['auth_user_id'] == log_dict['auth_user_id']
    
# def test_register_invalid_email():
#     user_info = {"email": "abcd.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400

# def test_register_exist_email():
#     user1_info = {"email": "aa@gmail.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
#     requests.post(config.url + 'auth/register/v2', json = user1_info)
#     user2_info = {"email": "aa@gmail.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
#     assert requests.post(config.url + 'auth/register/v2', json = user2_info).status_code == 400                             

# def test_register_short_password():
#     user_info = {"email": "a@gmail.com", "password": "abcd", "name_first": "a", "name_last": "c"}
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400

# def test_register_no_name_first():
#     user_info = {"email": "b@gmail.com", "password": "abcdcdf", "name_first": "", "name_last": "c"}
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400
      
# def test_register_long_name_first(): 
#     user_info = {"email": "ab@g.com", "password": "abcdefg",
#                 "name_first": "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu", "name_last": "c"}     
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400

# def test_register_no_name_last():
#     user_info = {"email": "c@gmail.com", "password": "abcdcdf", "name_first": "a", "name_last": ""}
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400

# def test_register_long_name_last():
#     user_info =  {"email": "d@gmail.com", "password": "abcdcdf",
#                 "name_first": "a", "name_last": "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu"}
#     assert requests.post(config.url + 'auth/register/v2', json = user_info).status_code == 400