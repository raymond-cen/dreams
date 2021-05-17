import pytest
import requests
from src.auth import create_token
from src import config
from src.error import InputError
from src.data import data


def test_lists_v2():
    user1 = {"email": "l3nin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "channel_name": "week1", "is_public": True}
    requests.post(f"{config.url}channels/create/v2", json=channel_info)
    token_list = {"token": reg_user1_json["token"]}
    channel_list = requests.get(f"{config.url}channels/list/v2", params = token_list)
    assert channel_list.status_code == 200


def test_2_channels_v2():
    user1 = {"email": "lenin2@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "channel_name": "xavi", "is_public": True}
    requests.post(f"{config.url}channels/create/v2", json=channel_info)
    channel_info2 = {"token": reg_user1_json["token"], "channel_name": "week2", "is_public": True}
    requests.post(f"{config.url}channels/create/v2", json=channel_info2)
    token_list = {"token": reg_user1_json["token"]}
    channel_list = requests.get(f"{config.url}channels/list/v2", params=token_list)
    assert channel_list.status_code == 200


def test_no_channels_v2():
    user1 = {"email": "lenin3@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    token_list = {"token": reg_user1_json["token"]}
    channel_list = requests.get(f"{config.url}channels/list/v2", params=token_list)
    assert channel_list.status_code == 200


def test_invalid_token_v2():
    user1 = {"email": "lenin4@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "channel_name": "week1", "is_public": True}
    requests.post(f"{config.url}channels/create/v2", json=channel_info)
    token_list = {"token": create_token (313132,1)}
    channel_list = requests.get(f"{config.url}channels/list/v2", params=token_list)
    assert channel_list.status_code == 403
