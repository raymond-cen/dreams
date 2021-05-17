import requests
import pytest
import json
from src import config
from src.auth import create_token
from src.error import InputError, AccessError
from src.other import clear_v1
# still debugging 
def test_join_public():

    user1_info = {"email": "eur@gail.com", "password": "123456", "name_first": "ab", "name_last": "cd"} 
    global user1
    user1 = requests.post(config.url + 'auth/register/v2', json = user1_info)    
    global user1_dict
    user1_dict = user1.json()
    
    channel1_info = {"token" : user1_dict['token'], "name": "week1", "is_public": True}
    global channel1
    channel1 = requests.post(config.url + 'channels/create/v2', json = channel1_info)
    global channel1_dict
    channel1_dict = channel1.json()
    
    user2_info = {"email": "223@yaoo.com", "password": "123ac!#", "name_first": "y", "name_last": "k"}  
    global user2
    user2 = requests.post(config.url + 'auth/register/v2', json = user2_info)
    global user2_dict
    user2_dict = user2.json()
    
    join_info = {"token" : user2_dict['token'], "channel_id": channel1_dict['channel_id']}
    result1 = requests.post(config.url + 'channel/join/v2', json = join_info)
   
    assert result1.status_code == 200

def test_join_private_global_owner():
    channel2_info = {"token": user2_dict['token'], "name": 'hi', "is_public": False}
    global channel2
    channel2 = requests.post(config.url + 'channels/create/v2', json = channel2_info)
    global channel2_dict
    channel2_dict = channel2.json()
    token = create_token(1, 1)
    join_info = {"token" : token, "channel_id": channel2_dict['channel_id']}
    result2 = requests.post(config.url + 'channel/join/v2', json = join_info)
    assert result2.status_code == 200

def test_join_invalid_channel_id():
    join_info = {"token" : user1_dict['token'], "channel_id": -1}
    assert requests.post(config.url + 'channel/join/v2', json = join_info).status_code == 400
    
def test_join_invalid_permission():
    user3_info = {"email" : "yu.ee@ol.com", "password": "123abc!@", "name_first": "yzu", "name_last": "key"}
    global user3
    user3 = requests.post(config.url + 'auth/register/v2', json = user3_info)
    global user3_dict
    user3_dict = user3.json()
    join_info = {"token" : user3_dict['token'], "channel_id": channel2_dict['channel_id']}
    assert requests.post(config.url + 'channel/join/v2', json = join_info).status_code == 403

def test_join_invalid_user_id():
    bad_token = create_token(-7, 1)
    join_info = {"token" : bad_token, "channel_id": channel1_dict['channel_id']}
    assert requests.post(config.url + 'channel/join/v2', json = join_info).status_code == 400
  
def test_join_member_rejoin():
    join1_info = {"token" : user3_dict['token'], "channel_id": channel1_dict['channel_id']}
    requests.post(config.url + 'channel/join/v2', json = join1_info)
    join2_info = {"token" : user3_dict['token'], "channel_id": channel1_dict['channel_id']}
    assert requests.post(config.url + 'channel/join/v2', json = join2_info).status_code == 403
