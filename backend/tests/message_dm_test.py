import pytest
from src.message import message_senddm_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_valid_dm():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    assert message_senddm_v1(token['token'], dm1['dm_id'], "message") == {'message_id': 1}

def test_invaliddm():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    with pytest.raises(InputError):
        message_senddm_v1(token['token'], dm1['dm_id'] + 23213, "message")


def test_not_in_dm():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    with pytest.raises(AccessError):
        message_senddm_v1(token3['token'], dm1['dm_id'], "message")

def test_too_long_message():
    # over 1000 characters long message
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = "hi"
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        message_senddm_v1(token['token'], dm1['dm_id'], message)
