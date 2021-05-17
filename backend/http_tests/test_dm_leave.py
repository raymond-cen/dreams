import requests
from src.auth import create_token
from src import config, data
from src.data import data


def test_dm_leave():

    user1 = {"email": "lenxfin76xf@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify=False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "fiaf32del@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    user3 = {"email": "r3245faul@castro.com", "password": "cubaandfidel", "name_first": "raul", "name_last": "castro"}
    reg_user3 = requests.post(f'{config.url}auth/register/v2', json=user3)
    reg_user3_json = reg_user3.json()
    dm_info = {"token": reg_user1_json["token"], "u_ids": [reg_user2_json["auth_user_id"], reg_user3_json["auth_user_id"]]}
    dm_c = requests.post(f'{config.url}dm/create/v1', json=dm_info)
    dm_cjson = dm_c.json()
    info_dict = {"token": reg_user3_json["token"], "dm_id": dm_cjson["dm_id"]}
    dm_l = requests.post(f'{config.url}dm/leave/v1', json=info_dict)
    assert dm_l.status_code == 200


def test_not_valid_token():

    user1 = {"email": "lefxg435nin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify=False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "fidfh534el@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    user3 = {"email": "234fxgraul@castro.com", "password": "cubaandfidel", "name_first": "raul", "name_last": "castro"}
    reg_user3 = requests.post(f'{config.url}auth/register/v2', json=user3)
    reg_user3_json = reg_user3.json()
    dm_info = {"token": reg_user1_json["token"],
               "u_ids": [reg_user2_json["auth_user_id"], reg_user3_json["auth_user_id"]]}
    dm_c = requests.post(f'{config.url}dm/create/v1', json=dm_info)
    dm_cjson = dm_c.json()
    info_dict = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjkwLCJzZXNzaW9uX2lkIjoxfQ"
                          ".bBZYT990ObCQBxyYbXc-rwq6vONVMxmDW-Xx6GRDwSM", "dm_id": dm_cjson["dm_id"]}
    dm_l = requests.post(f'{config.url}dm/leave/v1', json=info_dict)
    assert dm_l.status_code == 403


def test_not_a_valid_dm():

    user1 = {"email": "len643xfgin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1, verify=False)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "fid5w6sfel@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    user3 = {"email": "raul435dzf@castro.com", "password": "cubaandfidel", "name_first": "raul", "name_last": "castro"}
    reg_user3 = requests.post(f'{config.url}auth/register/v2', json=user3)
    reg_user3_json = reg_user3.json()
    dm_info = {"token": reg_user1_json["token"],
               "u_ids": [reg_user2_json["auth_user_id"], reg_user3_json["auth_user_id"]]}
    dm_c = requests.post(f'{config.url}dm/create/v1', json=dm_info)
    dm_c.json()
    info_dict = {"token": reg_user3_json["token"],"dm_id": 800}
    dm_l = requests.post(f'{config.url}dm/leave/v1', json=info_dict)
    assert dm_l.status_code == 400
