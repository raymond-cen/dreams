"""testcases for channel_details_v1 function in channel
assumptions:
    - u_id is user id
    - channel_id is channel name
"""
#need to check that user is part of channel before giving details
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.data import data
from src.other import clear_v1
import pytest

#Unauthorised users adding members to channel
def test_invalid():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          

    cid1 = channels_create_v1(uid1['token'], 'harry_channel1', True)
    cid2 = channels_create_v1(uid2['token'], 'jane_channel2', True)
    # Auth user not in channel
    with pytest.raises(AccessError):
        channel_invite_v1(uid2['token'], cid1['channel_id'], uid1['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(uid1['token'], cid2['channel_id'], uid2['auth_user_id'])
    # invalid channel id
    with pytest.raises(InputError):
        channel_invite_v1(uid2['token'], 123314, uid1['token'])

#Authorised user adds member to channel
def test_success():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          

    cid1 = channels_create_v1(uid1['token'], 'harry_channel1', True)
    cid2 = channels_create_v1(uid2['token'], 'jane_channel2', True)

    assert channel_invite_v1(uid2['token'], cid2['channel_id'], uid1['auth_user_id']) == {}
    assert channel_invite_v1(uid1['token'], cid1['channel_id'], uid2['auth_user_id']) == {}
