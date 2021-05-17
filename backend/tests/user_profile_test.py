from src.user import user_profile_v1
from src.auth import auth_register_v1, create_token
from src.error import InputError, AccessError
from src.other import clear_v1
import pytest

def test_profile_success():
    # clear_v1()
    global user
    user = auth_register_v1("abcd321@gmail.com", "123456", "ab", "cd")    
    ret_user = user_profile_v1(user['token'], user['auth_user_id']) 
    
    assert ret_user['user']['u_id'] == user['auth_user_id']
    assert ret_user['user']['email'] == "abcd321@gmail.com"
    assert ret_user['user']['name_first'] == "ab"
    assert ret_user['user']['name_last'] == "cd"
    assert ret_user['user']['handle_str'] == "ab" + "cd3"

def test_profile_invalid_id():
    with pytest.raises(InputError):
        user_profile_v1(user['token'], -1)

def test_profile_invalid_token():
    bad_token = create_token(-1, 1)
    with pytest.raises(AccessError):
        user_profile_v1(bad_token, user['auth_user_id'])