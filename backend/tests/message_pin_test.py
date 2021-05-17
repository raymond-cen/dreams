import pytest
import time
from src.message import message_send_v2, message_pin_v1, message_senddm_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def create_channel():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    message_id = message_send_v2(token['token'], channel1['channel_id'], "message")
    return token['token'], channel1['channel_id'], message_id['message_id']

@pytest.fixture
def create_dm():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token1 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token1['auth_user_id']])
    m_id = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    return token['token'], dm1['dm_id'], m_id['message_id']

def test_success_channel(create_channel):
    token, _, m_id = create_channel
    assert message_pin_v1(token, m_id) == {}

def test_non_auth_user_channel(create_channel):
    _, _, m_id = create_channel
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        message_pin_v1(token2['token'], m_id)

def test_message_already_pinned(create_channel):
    token, _, m_id = create_channel
    message_pin_v1(token, m_id)
    with pytest.raises(InputError):
        message_pin_v1(token, m_id)

def test_invalid_message(create_channel):
    token, _, m_id = create_channel
    with pytest.raises(InputError):
        message_pin_v1(token, m_id + 12)

def test_success_dm(create_dm):
    token, _, m_id = create_dm
    assert message_pin_v1(token, m_id) == {}

def test_invalid_auth_user_dm(create_dm):
    _, _, m_id = create_dm
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        message_pin_v1(token3['token'], m_id)
    
def test_message_already_reacted_dm(create_dm):
    token, _, m_id = create_dm
    message_pin_v1(token, m_id)
    with pytest.raises(InputError):
        message_pin_v1(token, m_id)

def test_invalid_message_dm(create_dm):
    token, _, m_id = create_dm
    with pytest.raises(InputError):
        message_pin_v1(token, m_id + 123)
