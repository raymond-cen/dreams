import pytest
from src.auth import auth_register_v1, create_token, decode_token
from src.data import data
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_send_v2, message_senddm_v1
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture
def create_all():
    clear_v1()
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token1 = auth_register_v1("validemail2@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token1['auth_user_id']])
    return token, dm1

def test_invalid_token(create_all):
    _, dm1 = create_all
    print(dm1)
    invalid_token = create_token(1230,213)
    
    # Check if user_id is a member of the dm
    with pytest.raises(AccessError):
        dm_messages_v1(invalid_token, dm1['dm_id'], 0)

# Start is greater than the amount of messages in dm
def test_invalid_start(create_all):
    token, dm1 = create_all
    with pytest.raises(InputError):
        dm_messages_v1(token['token'], dm1['dm_id'], 100)    
def test_invalid_dm(create_all):
    token, dm1 = create_all
    # Check invalid dm id
    invalid_dm_id = dm1['dm_id'] + 1000
    with pytest.raises(InputError):
        dm_messages_v1(token['token'], invalid_dm_id, 0)



def test_succeed_no_message():
    # Succeed with no messages
    clear_v1() 
    token = auth_register_v1("validemail@gmail.com", "123456", "ab", "cd")
    token1 = auth_register_v1("validemail22@gmail.com", "123456", "ab", "cd")
    dm1 = dm_create_v1(token['token'], [token1['auth_user_id']])
    assert dm_messages_v1(token["token"], dm1['dm_id'], 0) == {
                                                                                    'messages': [],
                                                                                    'start': 0,
                                                                                    'end': -1,
                                                                                }
def test_succeed(create_all):
    # Succeed with 1 messages
    token, dm1 = create_all
    m_id = message_senddm_v1(token['token'], dm1['dm_id'], "message")
    assert dm_messages_v1(token["token"], dm1['dm_id'], 0) == {
                                                                                    'messages': [{
                                                                                    'message_id': m_id['message_id'],
                                                                                    'u_id': decode_token(token['token']),
                                                                                    'message': 'message',
                                                                                    'time_created': data['message']['message_info'][0]['time_created'],
                                                                                    'reacts': [{'is_this_user_reacted': False, 'react_id': 0, 'u_ids': []}],
                                                                                    'is_pinned': False
                                                                                }],
                                                                                    'start': 0,
                                                                                    'end': -1,
                                                                                }

def test_succeed_50_messages(create_all):
    # Succeed with 50 messages
    token, dm1 = create_all
    message_list = []
    for _ in range(50):
        m_id = message_senddm_v1(token['token'], dm1['dm_id'], "message")
        message_info = {
                        'message_id': m_id['message_id'],
                        'u_id': decode_token(token['token']),
                        'message': 'message',
                        'time_created': data['message']['message_info'][0]['time_created'],
                        'reacts': [{'is_this_user_reacted': False, 'react_id': 0, 'u_ids': []}],
                        'is_pinned': False
                    }
        message_list.append(message_info)
    message_list.reverse()
    assert dm_messages_v1(token["token"], dm1['dm_id'], 0) == {
                                                                                    'messages': message_list,
                                                                                    'start': 0,
                                                                                    'end': -1,
                                                                                }
def test_different_start(create_all):
    # Succeed with 50 messages
    token, dm1 = create_all
    message_list = []
    for x in range(100):
        m_id = message_senddm_v1(token['token'], dm1['dm_id'], "message" + str(x))
        message_info = {
                    'message_id': m_id['message_id'],
                    'u_id': decode_token(token['token']),
                    'message': "message" + str(x),
                    'time_created': data['message']['message_info'][0]['time_created'],
                    'reacts': [{'is_this_user_reacted': False, 'react_id': 0, 'u_ids': []}],
                    'is_pinned': False
                }
        message_list.append(message_info)
    message_list.reverse()
    assert dm_messages_v1(token["token"], dm1['dm_id'], 49) == {
                                                                                    'messages': message_list[49:99],
                                                                                    'start': 49,
                                                                                    'end': 99,
                                                                                }
