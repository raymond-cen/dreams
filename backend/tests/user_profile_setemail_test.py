from src.user import user_profile_setemail_v1
from src.auth import auth_register_v1,create_token
from src.error import InputError, AccessError
import pytest 

def test_setemail_success():
    global user
    user = auth_register_v1("abcd@gmil.com", "123456", "ab", "cd")    
    assert user_profile_setemail_v1(user['token'], "ad@gmail.com") == {}

def test_setemail_invalid_email():
    with pytest.raises(InputError):
        user_profile_setemail_v1(user['token'], "bad.com")

def test_setemail_existed_for_another_user():
    auth_register_v1("aaa@gmal.com", "1234576", "abc", "d")
    with pytest.raises(InputError):
        user_profile_setemail_v1(user['token'], "aaa@gmal.com")

def test_setemail_invalid_token():
    bad_token = create_token(-1, 1)
    with pytest.raises(AccessError):
        user_profile_setemail_v1(bad_token, "bad@yah.com")