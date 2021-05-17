import pytest
import time
from src.message import message_sendlaterdm_v1, message_send_v2
from src.auth import auth_register_v1, create_token
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def create_all():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token1 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token1['auth_user_id']])
    return token['token'], dm1['dm_id']

def test_success(create_all):
    token, dm1 = create_all
    assert message_sendlaterdm_v1(token, dm1, 'message', time.time() + 1) == {'message_id': 1}

def test_invaliddm(create_all):
    token, dm1 = create_all
    with pytest.raises(InputError):
        message_sendlaterdm_v1(token, dm1 + 22, 'message', time.time() + 1)

def test_long_message(create_all):
    token, dm1 = create_all
    message = "hi"
    # create a long message
    for _ in range(10):
        message += message
    with pytest.raises(InputError):
        message_sendlaterdm_v1(token, dm1, message, time.time() + 1)

def test_invalid_time(create_all):
    token, dm1 = create_all
    with pytest.raises(InputError):
        message_sendlaterdm_v1(token, dm1,'message', time.time() - 100)

def test_invalid_auth_user(create_all):
    _, dm1 = create_all
    token3 = auth_register_v1("validemail3@gmail.com", "123456", "ab", "cd")
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(token3['token'], dm1,'message', time.time())

def test_user(create_all):
    _, dm1 = create_all
    with pytest.raises(InputError):
        message_sendlaterdm_v1(create_token(22,1), dm1,'message', time.time())


