from src.user import user_profile_sethandle_v1
from src.auth import auth_register_v1, create_token
from src.error import InputError, AccessError
import pytest 

def test_sethandle_success():
    global user
    user = auth_register_v1("abcd@gmail.com", "123456", "ab", "cd")    
    assert user_profile_sethandle_v1(user['token'], "aaaaaa") == {}

def test_sethandle_less_handle():
    with pytest.raises(InputError):        
        user_profile_sethandle_v1(user['token'], "aa")
      
def test_sethandle_long_handle(): 
    with pytest.raises(InputError):        
        user_profile_sethandle_v1(user['token'], "shhusensiheuiauhieydehuaheu")

def test_sethandle_existed_for_another_user():
    auth_register_v1("aa@gmail.com", "1234576", "aa", "bb")
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user['token'], "aabb")

def test_sethandle_invalid_token():
    bad_token = create_token(-1, 1)
    with pytest.raises(AccessError):
        user_profile_sethandle_v1(bad_token, "bad")