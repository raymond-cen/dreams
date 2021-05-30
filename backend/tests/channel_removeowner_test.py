from src.channel import channel_removeowner_v1, channel_addowner_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1, create_token
from src.error import InputError, AccessError
from src.other import clear_v1
import pytest

def test_remove_success():
    clear_v1()
    global user1
    user1 = auth_register_v1("abcd@gmail.com", "123456", "ab", "cd")
    global channel
    channel = channels_create_v1(user1['token'], 'week1', True)
    
    global user2 
    user2 = auth_register_v1("y.k@yahoo.com", "123ac!#", "y", "k")
    channel_addowner_v1(user1['token'], channel['channel_id'], user2['auth_user_id'])
    assert channel_removeowner_v1(user1['token'], channel['channel_id'], user2['auth_user_id']) == {}

def test_removeowner_invalid_channel(): 
    with pytest.raises(InputError):
        channel_removeowner_v1(user1['token'], -1, user2['auth_user_id'])

# u_id not owner of channel
def test_removeowner_invalid_owner():
    user3 = auth_register_v1("shufwfiw@vireo.com", "aeuiwf", "dewu", "heuw")
    with pytest.raises(InputError):
        channel_removeowner_v1(user1['token'], channel['channel_id'], user3['auth_user_id'])


def test_removeowner_only_owner():
    with pytest.raises(InputError):
        channel_removeowner_v1(user1['token'], channel['channel_id'], user1['auth_user_id'])

# token not golbal or owner of channel
def test_removeowner_not_owner():
    user4 = auth_register_v1("wehuie@ewpok.com", "hwefuai", "se", "wed")
    with pytest.raises(AccessError):
        channel_removeowner_v1(user4['token'], channel['channel_id'], user1['auth_user_id'])

 # invalid u_id from token       
def test_removeowner_invalid_user():
    bad_token = create_token(-1, 1)
    with pytest.raises(AccessError):
        channel_removeowner_v1(bad_token, channel['channel_id'], user1['auth_user_id'])
