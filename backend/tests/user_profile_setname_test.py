from src.user import user_profile_setname_v1
from src.auth import auth_register_v1,create_token
from src.error import InputError, AccessError
import pytest 

def test_setname_success():
    global user
    user = auth_register_v1("abcd@gail.com", "123456", "ab", "cd")    
    assert user_profile_setname_v1(user['token'], "aa", "bb") == {}

def test_setname_no_first_name():
    with pytest.raises(InputError):        
        user_profile_setname_v1(user['token'], "", "c")
      
def test_setname_long_first_name(): 
    with pytest.raises(InputError):        
        user_profile_setname_v1(user['token'],
                "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu", "c")  

def test_setname_no_last_name():
    with pytest.raises(InputError):        
        user_profile_setname_v1(user['token'], "a", "")

def test_setname_long_last_name():
    with pytest.raises(InputError):        
        user_profile_setname_v1(user['token'],
                "a", "shhusensiheuiauhieydehuaheujaijaomaodfvhuhweoavnzujeu")
   
def test_setname_invalid_token():
    bad_token = create_token(-1, 1)
    with pytest.raises(AccessError):
        user_profile_setname_v1(bad_token, "q", "w")