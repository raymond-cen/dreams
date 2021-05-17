import pytest
from src.message import message_remove_v1, message_send_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# TESTS FOR message_send

def test_valid_send():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    assert message_send_v2(token['token'], channel1['channel_id'], "message1") == {"message_id": 1}

    assert message_send_v2(token['token'], channel1['channel_id'], "message2") == {"message_id": 2}

def test_too_long_message():
    # over 1000 characters long message
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message = "hi"
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        message_send_v2(token['token'], channel1['channel_id'], message)

def test_non_auth_user():
    # over 1000 characters long message
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "bob", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)

    with pytest.raises(AccessError):
        message_send_v2(token2['token'], channel1['channel_id'], "message")
    with pytest.raises(InputError):
        message_send_v2(token['token'] + 'invalid4sure', channel1['channel_id'], "message")

def test_invalid_channelid():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    with pytest.raises(InputError):
        message_send_v2(token['token'], channel1['channel_id'] + 421, "message")
