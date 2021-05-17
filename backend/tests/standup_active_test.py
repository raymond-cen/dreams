import pytest
import time
from src.standup import standup_start_v1, standup_active_v1
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

def test_inactive(create_all):
    token, channel1 = create_all
    assert standup_active_v1(token, channel1) == {
                                                    'is_active': False,
                                                    'time_finish': None
                                                }
def test_active(create_all):
    token, channel1 = create_all
    standup_start_v1(token, channel1, 2)
    assert standup_active_v1(token, channel1) == {
                                                    'is_active': True,
                                                    'time_finish': int(time.time() + 2)
                                                }
def test_invalid_channel(create_all):
    token, channel1 = create_all
    standup_start_v1(token, channel1, 1)
    with pytest.raises(InputError):
        standup_active_v1(token, channel1 + 12)
