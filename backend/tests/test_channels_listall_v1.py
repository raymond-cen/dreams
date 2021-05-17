import jwt

from src.auth import auth_register_v1, create_token
from src.channels import channels_listall_v1
from src.channels import channels_create_v1
from src.error import AccessError
from src.data import data
from src.other import clear_v1
import pytest


def test_channels_all_list():
    clear_v1()
    # creating a user
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    # creating another channel with the auth_id 3
    channels_create_v1(user1['token'], 'week1', True)
    channels_create_v1(user2['token'], 'week2', False)
    channels_create_v1(user1['token'], 'LM10', True)
    channels_create_v1(user1['token'], 'Xavi', True)
    assert channels_listall_v1(user1['token']) == {'channels': [{'channel_id': 1, 'name': 'week1'},
                                                   {'channel_id': 2, 'name': 'week2'},
                                                   {'channel_id': 3, 'name': 'LM10'},
                                                   {'channel_id': 4, 'name': 'Xavi'}]}
    assert channels_listall_v1(user2['token']) == {'channels': [{'channel_id': 1, 'name': 'week1'},
                                                   {'channel_id': 2, 'name': 'week2'},
                                                   {'channel_id': 3, 'name': 'LM10'},
                                                   {'channel_id': 4, 'name': 'Xavi'}]}


def test_no_channels():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    user3 = auth_register_v1('linbiao@general.com', 'whatever', 'lin', 'biao')
    assert channels_listall_v1(user1['token']) == {'channels': []}
    assert channels_listall_v1(user2['token']) == {'channels': []}
    assert channels_listall_v1(user3['token']) == {'channels': []}


def test_invalid_id():
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_listall_v1(create_token(1, 1))        


def test_get_list_all():
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    channels_create_v1(user1['token'], 'busi', True)
    channels_create_v1(user1['token'], 'andres', True)
    channels_create_v1(user1['token'], 'puyol', True)
    assert channels_listall_v1(user2['token']) == {'channels': [{'channel_id': 1, 'name': 'busi'},
                                                   {'channel_id': 2, 'name': 'andres'},
                                                   {'channel_id': 3, 'name': 'puyol'}]}
