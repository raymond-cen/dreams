from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.data import data
import pytest


def test_clear_v1():
    users = {'auth_user_id': 1, 'name': 'harry'}
    data['users'].append(users)
    users = {'auth_user_id': 2, 'name': 'ron'}
    data['users'].append(users)
    clear_v1()
    assert bool(data) == True


# def test_channels_clear():
#     users = {'auth_user_id': 1, 'name': 'harry'}
#     data['users'].append(users)
#     users = {'auth_user_id': 2, 'name': 'ron'}
#     data['users'].append(users)
#     channels_create_v1(1, 'lenin', True)
#     assert data == {'users': [{'auth_user_id': 1, 'name': 'harry'}, {'auth_user_id': 2, 'name': 'ron'}], 'channels' : [{'channel_id': 1, 'channel_name': 'lenin', 'is_public': True, 'owner_id' : 1, 'members' : [{'members_id' : [1]}], 'messages' : []} ]}
#     clear_v1()
#     assert data =={'users': [], 'channels': []}
