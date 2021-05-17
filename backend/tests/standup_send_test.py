import pytest
import time
from src.standup import standup_start_v1, standup_send_v1
from src.auth import auth_register_v1, create_token
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def create_all():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    return token['token'], channel1['channel_id']

def test_success_send(create_all):
    token, channel1 = create_all
    standup_start_v1(token, channel1, 2)
    assert standup_send_v1(token, channel1, 'message') == {}

def test_invalidchannel(create_all):
    token, channel1 = create_all
    standup_start_v1(token, channel1, 2)
    with pytest.raises(InputError):
        standup_send_v1(token, channel1 + 5, 'message')
    
def test_long_message(create_all):
    token, channel1 = create_all
    standup_start_v1(token, channel1, 2)
    message = "hi"
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        standup_send_v1(token, channel1, message)

def test_inactive_standup(create_all):
    token, channel1 = create_all
    with pytest.raises(InputError):
        standup_send_v1(token, channel1, 'message')

def test_invalid_user(create_all):
    _, channel1 = create_all
    with pytest.raises(InputError):
        standup_send_v1(create_token(23,1), channel1, 'message')

def test_nonauth_user(create_all):
    _, channel1 = create_all
    token2 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        standup_send_v1(token2['token'], channel1, 'message')