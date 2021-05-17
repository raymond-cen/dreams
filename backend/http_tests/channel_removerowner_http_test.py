import requests
import json
from src import config
from src.error import InputError, AccessError
from src.auth import create_token 

def test_remove_success():
    user1_info = {"email": "wuivhe@jdl.com", "password": "123456", "name_first": "ab", "name_last": "cd"}
    global user1
    user1 = requests.post(config.url + 'auth/register/v2', json = user1_info)    
    global user1_dict
    user1_dict = user1.json()
    print(user1_dict)
    channel1_info = {"token": user1_dict['token'], "name": 'week1', "is_public": True}
    global channel1
    channel1 = requests.post(config.url + 'channels/create/v2', json = channel1_info)
    global channel1_dict
    channel1_dict = channel1.json()
    print(channel1_dict)
    #add owner
    user2_info = {"email": "evhiue@eivio.com", "password": "123ac!#", "name_first": "y", "name_last": "k"}
    global user2
    user2 = requests.post(config.url + 'auth/register/v2', json = user2_info)
    global user2_dict
    user2_dict = user2.json()
    print(user2_dict)
    add_info = {"token": user1_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": user2_dict['auth_user_id']}
    requests.post(config.url + 'channel/addowner/v1', json = add_info)
    remove_info = add_info
    #remove owner
    result = requests.post(config.url + 'channel/removeowner/v2', json = remove_info)
    print(result.json())
    assert result.status_code == 200

def test_removeowner_invalid_channel(): 
    add_info = {"token": user1_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": user2_dict['auth_user_id']}
    requests.post(config.url + 'channel/addowner/v1', json = add_info)   
    remove_info = {"token": user1_dict['token'], "channel_id": -1 , "u_id": user2_dict['auth_user_id']}
    assert requests.post(config.url + 'channel/removeowner/v2', json = remove_info).status_code == 400

# u_id not owner of channel
def test_removeowner_invalid_owner():
    remove_info = {"token": user1_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": -1}
    assert requests.post(config.url + 'channel/removeowner/v2', json = remove_info).status_code == 400

def test_removeowner_only_owner():
    remove1_info = {"token": user1_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": user2_dict['auth_user_id']}
    requests.post(config.url + 'channel/removeowner/v2', json = remove1_info)
    remove2_info = {"token": user1_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": user1_dict['auth_user_id']}
    assert requests.post(config.url + 'channel/removeowner/v2', json = remove2_info).status_code == 400

# token not golbal or owner of channel
def test_removeowner_not_owner():
    remove_info = {"token": user2_dict['token'], "channel_id": channel1_dict['channel_id'], "u_id": user1_dict['auth_user_id']}
    assert requests.post(config.url + 'channel/removeowner/v2', json = remove_info).status_code == 403

 # invalid u_id from token       
def test_removeowner_invalid_user():
    bad_token = create_token(-5, 1)
    remove_info = {"token": bad_token, "channel_id": channel1_dict['channel_id'], "u_id": user1_dict['auth_user_id']}
    assert requests.post(config.url + 'channel/removeowner/v2', json = remove_info).status_code == 403
       
