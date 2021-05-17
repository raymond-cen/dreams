import pytest

from src.auth import auth_register_v1
from src.dm import dm_invite_v1, dm_create_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data import data

def test_invalid():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          
    uid3 = auth_register_v1('ja3ne@gmail.com', 'Qawsed123#', 'jane', 'bui') 
    cid1 = dm_create_v1(uid1['token'], [uid2['auth_user_id']])
    # Auth user not in channel
    with pytest.raises(AccessError):
        dm_invite_v1(uid3['token'], cid1['dm_id'], uid1['auth_user_id'])
    with pytest.raises(InputError):
        dm_invite_v1(uid1['token'], cid1['dm_id'], uid1['auth_user_id'] + 213)

def test_invalid_dmid():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          
    uid3 = auth_register_v1('ja3ne@gmail.com', 'Qawsed123#', 'jane', 'bui') 
    cid1 = dm_create_v1(uid1['token'], [uid2['auth_user_id']])
    with pytest.raises(InputError):
        dm_invite_v1(uid1['token'], cid1['dm_id'] + 2131, uid3['auth_user_id'])

def test_valid():
    clear_v1()
    uid1 = auth_register_v1('harry@gmail.com', 'Qawsed123#', 'harry', 'shen')
    uid2 = auth_register_v1('jane@gmail.com', 'Qawsed123#', 'jane', 'bui')          
    uid3 = auth_register_v1('ja3ne@gmail.com', 'Qawsed123#', 'jane', 'bui') 
    cid1 = dm_create_v1(uid1['token'], [uid2['auth_user_id']])
    assert dm_invite_v1(uid1['token'], cid1['dm_id'], uid3['auth_user_id']) == {}