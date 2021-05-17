import pytest
import time
from src.standup import standup_start_v1
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

def test_standup_success(create_all):
    token, channel1 = create_all
    assert standup_start_v1(token, channel1, 1) == {'time_finished': int(time.time()) + 1}

def test_active_standup(create_all):
    token, channel1 = create_all
    assert standup_start_v1(token, channel1, 3) == {'time_finished': int(time.time()) + 3}
    with pytest.raises(InputError):
        assert standup_start_v1(token, channel1, 1)

def test_invalid_channel(create_all):
    token, channel1 = create_all
    with pytest.raises(InputError):
        standup_start_v1(token, channel1 + 2, 1)

def test_invalid_user(create_all):
    _, channel1 = create_all
    with pytest.raises(AccessError):
        standup_start_v1(create_token(20,1), channel1, 1)

    