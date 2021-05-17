from src.data import data, add_new_user
import pytest
from src.auth import auth_login_v1, auth_register_v1, decode_token, auth_logout_v1, auth_passwordreset_request_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_reset_succeed(): 
    clear_v1()
    user_register = auth_register_v1("fodish893h@gmail.com", "123456", "ab", "cd") 
    u_id = user_register['auth_user_id']

    auth_passwordreset_request_v1('fodish893h@gmail.com')

    index = -1
    user_no = len(data['users'])
    i = 0
    while i < user_no:
        if (data['users'][i]['auth_user_id'] == u_id):
            if ('password_reset' in data['users'][i]):
                index = i
        i+=1

    print(data['users'][index])
    assert 'password_reset' in data['users'][index]

def test_reset_email_not_exist(): 
    auth_passwordreset_request_v1('')

    assert '' not in data['users']