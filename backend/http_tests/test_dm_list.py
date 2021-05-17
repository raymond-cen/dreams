import requests
from src import config
from src.auth import create_token


def test_dm_list_imvalid():
    user1 = {"email": "lll5lenin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify = False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "ff15idel@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    dm_info = {"token": reg_user1_json["token"], "u_ids": [reg_user2_json["auth_user_id"]]}
    requests.post(f"{config.url}dm/create/v1", json = dm_info)
    dm_info2 = {"token": reg_user2_json["token"], "u_ids": [reg_user1_json["auth_user_id"]]}
    requests.post(f'{config.url}dm/create/v1', json=dm_info2)
    token_list2 = {"token": reg_user2_json['token']} 

    dmlist = requests.get(f"{config.url}dm/list/v1", params=token_list2)
    assert dmlist.status_code == 200
