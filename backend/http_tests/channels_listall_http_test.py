import requests
from src.auth import create_token
from src import config


def test_channels_listall_v2():
    user1 = {"email": "len23in342@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    user2 = {"email": "fidel1231@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user2 = requests.post(f'{config.url}auth/register/v2', json=user2)
    reg_user2_json = reg_user2.json()
    channel1 = {"token": reg_user1_json["token"], "channel_name": "week1", "is_public": True}
    channel2 = {"token": reg_user1_json["token"], "channel_name": "week2", "is_public": False}
    channel3 = {"token": reg_user1_json["token"], "channel_name": "week3", "is_public": True}
    channel4 = {"token": reg_user1_json["token"], "channel_name": "week4", "is_public": False}
    channel5 = {"token": reg_user2_json["token"], "channel_name": "week5", "is_public": False}
    requests.post(f"{config.url}channels/create/v2", json=channel1)
    requests.post(f"{config.url}channels/create/v2", json=channel2)
    requests.post(f"{config.url}channels/create/v2", json=channel3)
    requests.post(f"{config.url}channels/create/v2", json=channel4)
    requests.post(f"{config.url}channels/create/v2", json=channel5)
    token_list = {"token": reg_user1_json["token"]}
    channel_listall = requests.get(f"{config.url}channels/list/v2", params=token_list)
    assert channel_listall.status_code == 200


def test_channels_listall_invalid_v2():
    user1 = {"email": "len4Sin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "channel_name": "week1", "is_public": True}
    requests.post(f"{config.url}channels/create/v2", json=channel_info)
    token_list = {"token": create_token(313132,1)}
    channel_list = requests.get(f"{config.url}channels/list/v2", params=token_list)
    assert channel_list.status_code == 403
