import pytest
from src.message import message_edit_v2, message_remove_v1, message_send_v2, message_senddm_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_valid_remove():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channels_create_v1(token['token'], "channel1", True)
    channel2 = channels_create_v1(token['token'], "channel12", True)
    message_id = message_send_v2(token['token'], channel2['channel_id'], "message")
    message_id2 = message_send_v2(token['token'], channel2['channel_id'], "message2")
    assert message_remove_v1(token['token'], message_id2['message_id']) == {}
    assert message_remove_v1(token['token'], message_id['message_id']) == {}

def test_invalid_auth(): # valid user that does not have the right to remove message
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemaill@gmail.com", "123456", "bob", "cd")
    channel1 = channels_create_v1(token1['token'], "channel1", True)
    message_id = message_send_v2(token1['token'], channel1['channel_id'], "message")
    with pytest.raises(AccessError):
        message_remove_v1(token2['token'], message_id['message_id'])

def test_invalid_messageid():
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token1['token'], "channel1", True)
    message_id = message_send_v2(token1['token'], channel1['channel_id'], "message")
    with pytest.raises(InputError):
        message_remove_v1(token1['token'], message_id['message_id'] + 1123)

# NEED TO ADD A MESSAGE DM TEST
def test_valid_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    assert message_remove_v1(token['token'], message['message_id']) == {}

def test_not_in_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    with pytest.raises(AccessError):
        message_remove_v1(token3['token'], message['message_id'])
    with pytest.raises(AccessError):
        message_remove_v1(token2['token'], message['message_id'])
