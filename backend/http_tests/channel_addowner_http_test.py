import pytest
import requests
import json
from src import config
from src.auth import create_token

def test_addowner_valid():
    #Create user lenin and create channel
    user_info1 = {"email": "lenin@bolshvik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    global user_reg1
    user_reg1 = requests.post(f'{config.url}auth/register/v2', json = user_info1)
    global reg_dict1
    reg_dict1 = user_reg1.json()
    channel_info = {"token": reg_dict1["token"], "name": "week1", "is_public": True}
    global channel
    channel = requests.post(f"{config.url}channels/create/v2", json = channel_info)
    global channel_dict 
    channel_dict = channel.json()

    #Create user john doe 
    user_info2 = {"email": "johndoe@gmail.com", "password": "123456", "name_first": "john", "name_last": "doe"}
    global user_reg2
    user_reg2 = requests.post(config.url + 'auth/register/v2', json = user_info2)    
    global reg_dict2
    reg_dict2 = user_reg2.json()  
    
    #Lenin makes John owner
    addowner_info = {"token": reg_dict1["token"], "channel_id": channel_dict["channel_id"], "u_id": reg_dict2["auth_user_id"]}
    resp = requests.post(f'{config.url}channel/addowner/v1', json = addowner_info)
    assert resp.status_code == 200

def test_addowner_invalid_id():
    #Lenin makes John owner
    addowner_info = {"token": reg_dict1["token"], "channel_id": -1, "u_id": reg_dict2["token"]}
    resp = requests.post(f'{config.url}channel/addowner/v1', json = addowner_info)
    assert resp.status_code == 400

def test_addowner_already_owner(): 
    addowner_info = {"token": reg_dict1["token"], "channel_id": channel_dict["channel_id"], "u_id": reg_dict2["auth_user_id"]}
    requests.post(f'{config.url}channel/addowner/v1', json = addowner_info)
    resp= requests.post(f'{config.url}channel/addowner/v1', json = addowner_info)
    assert resp.status_code == 400

def test_addowner_not_owner():    
    user_info3 = {"email": "lerjdfevi@bolshvik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    user_reg3 = requests.post(f'{config.url}auth/register/v2', json = user_info3)
    reg_dict3 = user_reg3.json()
    user_info4 = {"email": "lerjdfevi@bolshk.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    user_reg4 = requests.post(f'{config.url}auth/register/v2', json = user_info4)
    reg_dict4 = user_reg4.json()
    addowner_info = {"token": reg_dict3["token"], "channel_id": channel_dict["channel_id"], "u_id": reg_dict4["auth_user_id"]}
    resp = requests.post(f'{config.url}channel/addowner/v1', json = addowner_info)
    assert resp.status_code == 403
 
 # invalid u_id from token       
def test_addowner_invalid_user():
    bad_token = create_token(-5, 1)
    add_info = {"token": bad_token, "channel_id": channel_dict['channel_id'], "u_id": reg_dict1['auth_user_id']}
    assert requests.post(config.url + 'channel/addowner/v1', json = add_info).status_code == 403
       