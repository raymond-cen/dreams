import pytest
from src.auth import auth_register_v1, create_token
from src.channel import channel_leave_v1, channel_join_v1
from src.channels import channels_create_v1
from src.message import message_send_v2
from src.error import InputError, AccessError
from src.other import clear_v1

def test_succeed():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    channel_join_v1(token2['token'], channel1['channel_id'])
    assert channel_leave_v1(token2['token'], channel1['channel_id']) == {}
    assert channel_leave_v1(token['token'], channel1['channel_id']) == {}


def test_invalid_auth():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_register_v1("validema2il@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    channel_join_v1(token2['token'], channel1['channel_id'])
    channel1 = channels_create_v1(token['token'], "channel1", True)
    with pytest.raises(AccessError):
        assert channel_leave_v1(token2['token'], channel1['channel_id']) == {}

def test_invalid_channelid():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(token['token'], "channel1", True)
    with pytest.raises(InputError):
        assert channel_leave_v1(token['token'] + 'invalidtoken', channel1['channel_id'] + 213) == {}