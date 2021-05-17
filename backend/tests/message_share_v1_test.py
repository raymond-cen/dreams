import pytest
from src.message import message_remove_v1, message_send_v2, message_share_v1, message_senddm_v1
from src.dm import dm_create_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1


def test_valid_send():
    clear_v1()
    token = auth_register_v1("validemai143l@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message_id = message_send_v2(token['token'], channel1['channel_id'], "message1")

    assert message_share_v1(token['token'], message_id['message_id'], "added message", channel1['channel_id'], -1) == {"shared_message_id": 2}

def test_non_auth_user():
    # over 1000 characters long message
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "bob", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message_id = message_send_v2(token['token'], channel1['channel_id'], "message1")
    with pytest.raises(AccessError):
        message_share_v1(token2['token'], message_id['message_id'], "added message", channel1['channel_id'], -1)

def test_invalid_messageid():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token1['token'], "channel1", True)
    message_id = message_send_v2(token1['token'], channel1['channel_id'], "message")
    with pytest.raises(InputError):
        message_share_v1(token1['token'], message_id['message_id'] + 21312, 'hi' ,channel1['channel_id'], -1)

def test_invalid_channelid():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message = message_send_v2(token['token'], channel1['channel_id'], "message")
    with pytest.raises(InputError):
        message_share_v1(token['token'], message['message_id'], 'hi' ,channel1['channel_id'] + 421, -1)

def test_invalid_dmid():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    with pytest.raises(InputError):
        message_share_v1(token['token'], message['message_id'], 'hi' , -1, dm1['dm_id'] + 123)

def test_invaliddm_messageid():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token['auth_user_id']])
    message_id = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    with pytest.raises(InputError):
        message_share_v1(token['token'], message_id['message_id'] + 21312, 'hi', -1, dm1['dm_id'])

def test_not_in_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    with pytest.raises(AccessError):
        message_share_v1(token3['token'], message['message_id'], 'hi' , -1, dm1['dm_id'])

def test_valid_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    assert message_share_v1(token['token'], message['message_id'], 'hi' , -1, dm1['dm_id']) == {"shared_message_id": 2} 
