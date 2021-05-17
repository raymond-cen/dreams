import pytest
from src.message import message_edit_v2, message_send_v2, message_senddm_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

@pytest.fixture
def create_all():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message_id = message_send_v2(token['token'], channel1['channel_id'], "message")
    return token, channel1, message_id

def test_valid_edit(create_all):
    token, _, _ = create_all
    token2 = auth_register_v1("validem21ail@gmail.com", "123456", "ab", "cd")
    channel2 = channels_create_v1(token['token'], "channel22", True)
    message = message_send_v2(token['token'], channel2['channel_id'], "hi")
    dm_create_v1(token['token'], [token2['auth_user_id']])
    assert message_edit_v2(token['token'], message['message_id'], "edited_message") == {}

def test_empty_string(create_all):
    token, _, message_id = create_all
    assert message_edit_v2(token['token'], message_id['message_id'], "") == {}

def test_too_long_message(create_all):
    # over 1000 characters long message
    token, _, message_id = create_all
    message = "hi "
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        message_edit_v2(token['token'], message_id['message_id'], message)

def test_invalid_auth(create_all): # valid user that does not have the right to remove message
    _, _, message_id = create_all
    token2 = auth_register_v1("validemaill@gmail.com", "123456", "bob", "cd")
    with pytest.raises(AccessError):
        message_edit_v2(token2['token'], message_id['message_id'], "new message")

def test_invalid_messageid(create_all):
    token1, channel1, message_id = create_all
    message_id = message_send_v2(token1['token'], channel1['channel_id'], "message")
    with pytest.raises(InputError):
        message_edit_v2(token1['token'], message_id['message_id'] + 7314, "new message")

def test_valid_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    assert message_edit_v2(token['token'], message['message_id'], "yep") == {}
    with pytest.raises(AccessError):
        message_edit_v2(token2['token'], message['message_id'], "new message")

def test_not_in_dm():
    # invalid channel id
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token2['auth_user_id']])
    message = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    with pytest.raises(AccessError):
        message_edit_v2(token3['token'], message['message_id'], "new message")
