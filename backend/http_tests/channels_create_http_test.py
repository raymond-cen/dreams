import jwt
import pytest
import requests
from src.auth import create_token
from src.data import data
from src.error import InputError, AccessError
from src import config
import json
from flask import session

from src.other import clear_v1


def test_create_channels_v2_succeed():
    user1 = {"email": "lenivwor@bolshvik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json = user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "name": "week1", "is_public": True}
    channels_create = requests.post(f"{config.url}channels/create/v2", json = channel_info)
    assert channels_create.status_code == 200


def test_extra_long_names():
    user1 = {"email": "lenlkjin@bolshevik.com", "password": "123456", "name_first": "vladmir", "name_last": "lenin"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "name": "Thischannelsnameistoolong", "is_public": True}
    channel_create = requests.post(f"{config.url}channels/create/v2", json=channel_info)
    assert channel_create.status_code == 400


def test_short_long_names():
    user1 = {"email": "fidfu65el@castro.com", "password": "123456", "name_first": "fidel", "name_last": "castro"}
    reg_user1 = requests.post(f'{config.url}auth/register/v2', json=user1)
    reg_user1_json = reg_user1.json()
    channel_info = {"token": reg_user1_json["token"], "name": "we", "is_public": True}
    channels_create = requests.post(f"{config.url}/channels/create/v2", json=channel_info)
    assert channels_create.status_code == 200


def test_inavlid_token():
    channel_info = {"token" : create_token(1234242, 87643), "name": "noid", "is_public": False }
    channel_create = requests.post(f"{config.url}/channels/create/v2", json=channel_info)
    assert channel_create.status_code == 403

