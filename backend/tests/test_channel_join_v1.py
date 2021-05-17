# tests for channel join
import pytest
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1, create_token
from src.other import clear_v1

def test_channel_join_public():    
    # Test for another member to join a public channel
    clear_v1()
    global user1
    user1 = auth_register_v1("abcd@gya.com", "123456", "ab", "cd")
    channel1 = channels_create_v1(user1['token'], 'week1', True)
    
    global user2 
    user2 = auth_register_v1("y.k@hoo.com", "123ac!#", "y", "k")
    assert channel_join_v1(user2['token'], channel1['channel_id']) == {}

def test_channel_join_global_owner_join_private():
    # Test for golbal owner to join a private channel other owned
    channel2 = channels_create_v1(user2['token'], 'hi', False)
    assert channel_join_v1(user1['token'], channel2['channel_id']) == {}
   
def test_channel_join_invalid_channel_id():
    clear_v1()
    global user1
    user1 = auth_register_v1("op@gmal.com", "123456", "ab", "cd")
    # Not a valid channel ID
    with pytest.raises(InputError):
        channel_join_v1(user1['token'], 1)    
    with pytest.raises(InputError):
        channel_join_v1(user1['token'], 25000)
    with pytest.raises(InputError):
        channel_join_v1(user1['token'], -200)

def test_channel_join_channel_private():
    global channel1
    global user2
    channel1 = channels_create_v1(user1['token'], 'week2', False)
    user2 = auth_register_v1("y.adk@yaho.com", "123ac!#", "y", "k")
    with pytest.raises(AccessError):
        channel_join_v1(user2['token'], channel1['channel_id'])

def test_channel_join_member_rejoin():
    global channel2
    channel2 = channels_create_v1(user2['token'], 'weekends', True)
    user3 = auth_register_v1("ya.ke@lol.com", "123abc!@", "yzu", "key")
    channel_join_v1(user3['token'], channel2['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1(user3['token'], channel2['channel_id'])

def test_channel_join_invalid_user_id():
    invalid_token = create_token(-7, 1)
    with pytest.raises(InputError):
        channel_join_v1(invalid_token, channel2['channel_id']) 
