from src.user import users_all_v1
from src.auth import auth_register_v1, create_token
from src.error import AccessError
import pytest

def test_users_all_success():
    global user
    user = auth_register_v1("zzz@gmail.com", "123456", "xc", "vb")    
    ret_dict = users_all_v1(user['token']) 
    ret_ls = ret_dict['users']
    num = user['auth_user_id'] - 1
    assert ret_ls[num]['u_id'] == user['auth_user_id']
    assert ret_ls[num]['email'] == "zzz@gmail.com"
    assert ret_ls[num]['name_first'] == "xc"
    assert ret_ls[num]['name_last'] == "vb"
    assert ret_ls[num]['handle_str'] == "xc" + "vb"


def test_users_all_invalid_token():
    bad_token = create_token(-5, 1)
    with pytest.raises(AccessError):
        users_all_v1(bad_token)
