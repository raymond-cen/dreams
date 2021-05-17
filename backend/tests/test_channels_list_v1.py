import jwt

from src.auth import auth_register_v1, create_token
from src.channels import channels_list_v1
from src.channels import channels_create_v1
from src.error import AccessError
from src.data import data
from src.other import clear_v1
import pytest

def test_channels_containing_list():
    # clearing the data before the implementation
    clear_v1()
    # creating a user
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    # adding the user to the data to create a channel using this dummy auth_id
    # calling the channels create id to to create a channel using the above auth_id
    channels_create_v1(user1['token'], 'week1', True)
    # adding this user to the data
    # creating another channel with the auth_id 2
    channels_create_v1(user2['token'], 'week2', False)
    assert channels_list_v1(user1['token']) == {'channels': [{'channel_id': 1, 'name': 'week1'}]}
    assert channels_list_v1(user2['token']) == {'channels': [{'channel_id': 2, 'name': 'week2'}]}


def test_channels_containing_list1():
    # similar test to above but adding a particular id multiple channels to test the return
    clear_v1()
    # creating a user
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    channels_create_v1(user1['token'], 'week1', True)
    # creating another channel with the auth_id
    channels_create_v1(user1['token'], 'week2', False)
    # adding id:7 to the week2 channel created above
    channels_create_v1(user2['token'], 'week3', False)
    assert channels_list_v1(user1['token']) == {'channels': [{'channel_id': 1, 'name': 'week1'},
                                                             {'channel_id': 2, 'name': 'week2'}]}
    assert channels_list_v1(user2['token']) == {'channels': [{'channel_id': 3, 'name': 'week3'}]}


def tests_channels_multiple_same_id():
    clear_v1()
    # this tests when one id created multiple channels
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    # id: 1 creates first channel
    channels_create_v1(user1['token'], 'AttackonTitan', True)
    # id: 1 creates second channel and so on
    channels_create_v1(user1['token'], 'Naruto', True)
    channels_create_v1(user1['token'], 'Hunterxhunter', True)
    channels_create_v1(user1['token'], 'FullMetalAlchemist', True)
    channels_create_v1(user1['token'], 'Codegeass', True)
    assert channels_list_v1(user1['token']) == {'channels': [{'channel_id': 1, 'name': 'AttackonTitan'},
                                                 {'channel_id': 2, 'name': 'Naruto'},
                                                 {'channel_id': 3, 'name': 'Hunterxhunter'},
                                                 {'channel_id': 4, 'name': 'FullMetalAlchemist'},
                                                 {'channel_id': 5, 'name': 'Codegeass'}]}


def test_access_error_id():
    clear_v1()
    with pytest.raises(AccessError):
        # testing with a user that does not exist in the data
        channels_list_v1(create_token(100, 100))        


def test_user_no_channels():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    channels_create_v1(user2['token'], 'AOT', True)
    # testing a user that is not in any of the channels
    assert channels_list_v1(user1['token']) == {'channels': []}
