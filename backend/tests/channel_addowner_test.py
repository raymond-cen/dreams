import jwt

from src.auth import auth_register_v1, create_token
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.channel import channel_addowner_v1
from src.channels import channels_create_v1
from src.error import AccessError
from src.data import data
from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import create_token, auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_addowner_v1, channel_details_v1
import pytest


def test_addowner_success():
    # clearing the data before the implementation
    clear_v1()
    # creating a user
    global user1
    global user2
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    global channel1
    channel1 = channels_create_v1(user1['token'], "channel1", True)

    #Making user2 an owner
    assert channel_addowner_v1(user1['token'], channel1['channel_id'], user2['auth_user_id']) == {}
    
def test_add_global_owner():
    channel2 = channels_create_v1(user2['token'], "channel2", False)
    assert channel_addowner_v1(user2['token'], channel2['channel_id'], 1) == {}

def test_addowner_invalid_channel():
    user3 = auth_register_v1("shufiw@vireo.com", "aeuiwf", "dewu", "heuw")
    with pytest.raises(InputError): 
        channel_addowner_v1(user1['token'], -1, user3['token'])

def test_addowner_again():
    with pytest.raises(InputError): 
        channel_addowner_v1(user1['token'], channel1['channel_id'], user2['auth_user_id'])

def test_not_a_owner():
    user4 = auth_register_v1("shueiw@vure.com", "wuivnw", "ad", "wfe")
    with pytest.raises(AccessError): 
        channel_addowner_v1(user4['token'], channel1['channel_id'], user2['auth_user_id'])


 # invalid u_id from token       
def test_removeowner_invalid_user():
    bad_token = create_token(-1, 1)
    channel = channels_create_v1(user2['token'], 'week1', True)
    with pytest.raises(AccessError):
        channel_addowner_v1(bad_token, channel['channel_id'], user2['auth_user_id'])