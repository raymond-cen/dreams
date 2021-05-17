import pytest
import time
from src.message import message_sendlater_v1, message_send_v2
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def create_all():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    return token['token'], channel1['channel_id']

def test_invalid_channel(create_all):
    token, channel1 = create_all
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel1 + 5, 'message', time.time() + 1)

def test_long_message(create_all):
    token, channel1 = create_all
    message = "hi"
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel1, message, time.time() + 1)

def test_invalid_time(create_all):
    token, channel1 = create_all
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel1,'message', time.time() - 100)

def test_invalid_user(create_all):
    _, channel1 = create_all
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        message_sendlater_v1(token2['token'], channel1,'message', time.time() + 1)

def test_success(create_all):
    token, channel1 = create_all
    m_id = message_sendlater_v1(token, channel1,'message', time.time())
    assert m_id == {'message_id': 1}
