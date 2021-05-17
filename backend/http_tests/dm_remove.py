import requests
from src import config
from src.auth import create_token


def test_remove():
    user1 = {"email": "lenmnbvin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify = False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "fidel@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    dm_info = {"token": reg_user1_json["token"], "u_ids": [reg_user2_json["auth_user_id"]]}
    dm_c = requests.post(f'{config.url}dm/create/v1', json = dm_info)
    dm_cjson = dm_c.json()
    token_list = {"token": reg_user1_json["token"], "dm_id": dm_cjson["dm_id"]}
    dm_remove = requests.delete(f'{config.url}dm/remove/v1', json = token_list)
    assert dm_remove.status_code == 200


def test_invalid_dm_id():
    user1 = {"email": "lenghj32in@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify=False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "f1111l@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    dm_info = {"token": reg_user1_json["token"], "u_ids": [reg_user2_json["auth_user_id"]]}
    requests.post(f'{config.url}dm/create/v1', json=dm_info)
    token_list = {"token": reg_user1_json["token"], "dm_id": 933}
    dm_remove = requests.delete(f'{config.url}dm/remove/v1', json = token_list)
    assert dm_remove.status_code==400


# def test_non_creator_removing():
#     c = requests.delete(f'{config.url}clear/v1')
#     c.json()
#     user1 = {"email": "lenin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
#     reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify=False)
#     reg_user1_json = reg_user1.json()
#     user2 = {"email": "fidel@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
#     reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
#     reg_user2_json = reg_user2.json()
#     dm_info = {"token": reg_user1_json["token"], "u_id": [reg_user2_json["auth_user_id"]]}
#     dm_c = requests.post(f'{config.url}dm/create/v1', json=dm_info)
#     dm_cjson = dm_c.json()
#     token_list = {"token": reg_user2_json["token"], "dm_id": dm_cjson["dm_id"]}
#     dm_remove = requests.delete(f'{config.url}dm/remove/v1', json=token_list)
#     assert dm_remove.status_code == 403
