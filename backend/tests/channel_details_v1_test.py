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

def test_success():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          

    #Harry makes channel
    cid1 = channels_create_v1(uid1['token'], 'harry_channel1', True)
    # #Jane makes channel
    cid2 = channels_create_v1(uid2['token'], 'jane_channel2', True)
    # #Robert makes channel  
    assert channel_details_v1(uid1['token'], cid1['channel_id']) == {
                                                                            'name': 'harry_channel1',
                                                                            'owner_members': [
                                                                                {
                                                                                    'u_id': uid1['auth_user_id'],
                                                                                    'name_first': 'harry',
                                                                                    'name_last': 'shen',
                                                                                }
                                                                            ],
                                                                            'all_members': [
                                                                                {
                                                                                    'u_id': uid1['auth_user_id'],
                                                                                    'name_first': 'harry',
                                                                                    'name_last': 'shen',
                                                                                }
                                                                            ]
                                                                        }
    assert channel_details_v1(uid2['token'], cid2['channel_id']) == {       
                                                                            'name': 'jane_channel2',
                                                                            'owner_members': [
                                                                                {
                                                                                    'u_id': uid2['auth_user_id'],
                                                                                    'name_first': 'jane',
                                                                                    'name_last': 'bui',
                                                                                }
                                                                            ],
                                                                            'all_members': [
                                                                                {
                                                                                    'u_id': uid2['auth_user_id'],
                                                                                    'name_first': 'jane',
                                                                                    'name_last': 'bui',
                                                                                }
                                                                            ]}
    
#Unauthorised access
def test_unauthorised_access():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          

    #Harry makes channel
    cid1 = channels_create_v1(uid1['token'], 'harry_channel1', True)
    # #Jane makes channel
    cid2 = channels_create_v1(uid2['token'], 'jane_channel2', True)
    with pytest.raises(AccessError):
         channel_details_v1(uid1['token'], cid2['channel_id']) 
    with pytest.raises(AccessError):
         channel_details_v1(uid2['token'], cid1['channel_id']) 

#testing invalid channels
def test_invalid_channel():
    clear_v1()
    ud1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    with pytest.raises(InputError):
        channel_details_v1(ud1['token'], 5)

    with pytest.raises(InputError):
        channel_details_v1(ud1['token'], -1)

    with pytest.raises(InputError):
        channel_details_v1(ud1['token'], 10000)
    