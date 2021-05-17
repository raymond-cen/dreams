import time
import pytest
from src.other import search_v1, clear_v1
from src.auth import create_token, auth_register_v1
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.data import data

def test_search_channel_success():
    clear_v1()
    user = auth_register_v1("ewoj@gmail.com", "12345678", "aaa", "aa")
    channel = channels_create_v1(user['token'], "talk", True)
    message_send_v2(user['token'], channel['channel_id'], "message1")
    message_info = data['message']['message_info'][0]
    print(message_info)
    ret = search_v1(user['token'], "message")
    print(ret)
    assert ret == {'messages': [message_info]}
'''
def test_search_dm_success():
    user = auth_register_v1("woiea@gmail.com", "12345678", "aaa", "aa")
    dm = dm_create_v1(user['token'], user['auth_user_id'])
    m = message_senddm_v1(user['token'], dm['dm_id'], "hahaha")
    message_info = {'message_id': m['message_id'], 'u_id':  user['auth_user_id'], 'message': "message1", 'time_created': int(time.time())}
    assert search_v1(user['token'], "hahaha") == [message_info]
'''
def test_long_query_string():
    user = auth_register_v1("aarbba@gmail.com", "12345678", "aaa", "aa")
    query_str = "a"
    for i in range(0, 1002):
        query_str = query_str + str(i)
    with pytest.raises(InputError):
        search_v1(user['token'], query_str)

def test_invalid_id():
    bad_token = create_token(-5, 1)
    with pytest.raises(InputError):
        search_v1(bad_token, "haha")
