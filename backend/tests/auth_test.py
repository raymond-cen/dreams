import pytest
from src.auth import auth_login_v1, auth_register_v1, decode_token, auth_logout_v1
from src.other import clear_v1
from src.error import InputError, AccessError

def test_login_succeed(): # need to change login is not same as register anymore
    clear_v1()
    token1 = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token2 = auth_login_v1("validemail@gmail.com", "123456")
    assert decode_token(token1['token']) == decode_token(token2['token'])

def test_non_existing_email():
    with pytest.raises(InputError):
        auth_login_v1("emaildoesnot@gmail.com", "123456")

def test_invalid_email():
    with pytest.raises(InputError):
        auth_login_v1("invalidemail.com", "123456") 

def test_empty_arguments():
    with pytest.raises(InputError):
        auth_login_v1("", "")

def test_wrong_password():
    with pytest.raises(InputError):
        auth_login_v1("validemail@gmail.com", "wrongpassword")

def test_blank_password():
    with pytest.raises(Exception):
        auth_login_v1("validemail@gmail.com", "")


# Tests for auth register validity and exceptions
def test_register_valid_email():
    user_register = auth_register_v1("abcd@gmail.com", "123456", "ab", "cd") 
    user_login = auth_login_v1("abcd@gmail.com", "123456")
    assert user_register['auth_user_id'] == user_login['auth_user_id'] 

def test_register_whitespace_first_name():
    user_register = auth_register_v1("a.k@ak.com", "102acd", "a ", "kim")
    user_login = auth_login_v1("a.k@ak.com", "102acd")
    assert user_register['auth_user_id'] == user_login['auth_user_id']

def test_register_at_last_name():
    # Test for '@' first name
    user_register = auth_register_v1("jw.k@kr.com", "102acd", "jw", "kim@")
    user_login = auth_login_v1("jw.k@kr.com", "102acd")
    assert user_register['auth_user_id'] == user_login['auth_user_id']

def test_long_handle():
    user_register = auth_register_v1("kjw.k@kr.com", "102acd", "jwwhiosoensov", "kimheiosonv")
    user_login = auth_login_v1("kjw.k@kr.com", "102acd")
    assert user_register['auth_user_id'] == user_login['auth_user_id']

def test_register_invalid_email():
    with pytest.raises(InputError):
        auth_register_v1("abcd.com", "123456", "ab", "cd") 

def test_register_exist_email():
    auth_register_v1("aa@gmail.com", "123456", "ab", "cd")                             
    with pytest.raises(InputError):        
        auth_register_v1("aa@gmail.com", "abcdefg", "a", "c")                             

def test_register_short_password():   
    with pytest.raises(InputError):        
        auth_register_v1("a@gmail.com", "abcd", "a", "c")

def test_register_no_password():
    with pytest.raises(InputError):
        auth_register_v1("ha@ha.com", "", "ha", "ha")

def test_register_no_first_name():
    with pytest.raises(InputError):        
        auth_register_v1("bf@gmail.com", "abcdcdf", "", "c")
      
def test_register_long_first_name(): 
    with pytest.raises(InputError):        
        auth_register_v1("ab@g.com", "abcdefg",
                "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu", "c")  

def test_register_no_last_name():
    with pytest.raises(InputError):        
        auth_register_v1("cd@gmail.com", "abcdcdf", "a", "")

def test_register_long_last_name():
    with pytest.raises(InputError):        
        auth_register_v1("d@gmail.com", "abcdcdf",
                "a", "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu")
   
# auth_logout tests
def test_logout_succeed():
    token = auth_login_v1("validemail@gmail.com", "123456")
    assert auth_logout_v1(token['token']) == {"is_success": True}

def test_invalid_token():
    token = auth_login_v1("validemail@gmail.com", "123456")
    with pytest.raises(AccessError):
        auth_logout_v1(token['token'] + "invalidtoken")
        