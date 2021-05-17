import pytest
from src.auth import auth_register_v1, create_token, decode_token
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v2
from src.admin import admin_user_remove_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

def test_invalid_token():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    with pytest.raises(InputError):
        admin_user_remove_v1(token['token'] + "yesuhi", [token['auth_user_id']])

def test_not_owner():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        admin_user_remove_v1(token2['token'], [token1['auth_user_id']])

def test_invalid_uid():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    with pytest.raises(InputError):
        admin_user_remove_v1(token1['token'], [token2['auth_user_id'] + 21, token3['auth_user_id']])
    with pytest.raises(InputError):
        admin_user_remove_v1(token1['token'], [token2['auth_user_id'], token3['auth_user_id'] + 32])

def test_one_owner():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    with pytest.raises(InputError):
        admin_user_remove_v1(token1['token'], [token1['auth_user_id']])

def test_valid():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    assert admin_user_remove_v1(token1['token'], token2['auth_user_id']) == {}

    assert data['users'][1]['name_first'] + data['users'][1]['name_last'] == "RemovedUser"

def test_valid_message():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")

    channel1 = channels_create_v1(token1['token'], 'channelnamea', True)
    # not blackbox but w/e
    data['channels'][0]['members'][0]['members_id'].append(decode_token(token2['token']))
    data['channels'][0]['members'][0]['members_id'].append(decode_token(token3['token']))

    message_send_v2(token3['token'], channel1['channel_id'], "yepp")
    
    assert admin_user_remove_v1(token1['token'], token3['auth_user_id']) == {}
    assert data['message']['message_info'][0]['message'] == 'Removed User'
