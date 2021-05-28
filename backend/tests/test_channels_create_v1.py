import jwt

from src.auth import auth_register_v1, create_token
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.data import data
from src.other import clear_v1
import pytest



# to create a channel with valid auth_id and name


def test_channels_create():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    assert channels_create_v1(user1['token'], 'week1', True) == {'channel_id': 1}
    assert channels_create_v1(user2['token'], 'week2', False) == {'channel_id': 2}


# name more than 20 characters long


def test_long_names_except():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    with pytest.raises(InputError):
        assert channels_create_v1(user1['token'], "YesIamcreatinganewchannel", True)

def test_long_long_names_except():
    clear_v1()
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    with pytest.raises(InputError):
        assert channels_create_v1(user2['token'], "Averylongnameisamustforsecurityreasons", True)


# shorter names of the channel


def test_short_names():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    assert channels_create_v1(user1['token'], "abc", True) == {'channel_id': 1}
    assert channels_create_v1(user2['token'], "de", True) == {'channel_id': 2}



# invalid auth_id that do not exist in our data to create a channel


def test_invalid_bad_token():
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_create_v1(create_token(10, 10), "def", False)

def test_invalid_wrong_token():
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_create_v1(create_token(110, 120), 'allthatglittersisgold', True)
clear_v1()