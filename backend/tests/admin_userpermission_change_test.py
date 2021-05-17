import pytest
from src.auth import auth_register_v1, create_token, decode_token
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v2
from src.admin import admin_userpermission_change_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

def test_invalid_token():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(token['token'] + "yesuhi", token2['auth_user_id'], 1)

def test_invalid_permissionid():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    with pytest.raises(InputError):
        admin_userpermission_change_v1(token['token'], token2['auth_user_id'], 3)

def test_invalid_auth():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(token2['token'], token1['auth_user_id'], 2)

def test_valid():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    assert admin_userpermission_change_v1(token1['token'], token2['auth_user_id'], 1) == {}
        