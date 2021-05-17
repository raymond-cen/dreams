import pytest

from src.auth import auth_register_v1
from src.dm import dm_details_v1, dm_list_v1
from src.channels import channels_create_v1
from src.error import InputError
from src.error import AccessError
from src.data import data

def clear_v1():
    for key in data:
        data[key] = []

def test_list_dm():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    dmi = {'dm_id': 1, 'dm_name': 'fidelcastro,enverhoxha',
           'u_ids': [user1['auth_user_id'], user2['auth_user_id']],
           'owner': user1['auth_user_id']}
    data['dm'].append(dmi)
    user3 = auth_register_v1('thomas@sankara.com', 'burkinafaso', 'thomas', 'sankara')
    dmi = {'dm_id': 2, 'dm_name': 'fidelcastro,thomassankara',
           'u_ids': [user1['auth_user_id'], user3['auth_user_id']],
           'owner': user3['auth_user_id']}
    data['dm'].append(dmi)
    user4 = auth_register_v1('rosa@luxembourg.com', 'poland', 'rosa', 'luxembourg')
    dmi = {'dm_id': 3, 'dm_name': 'thomassankara,fidelcastro,enverhoxha',
           'u_ids': [user4['auth_user_id'], user1['auth_user_id'], user2['auth_user_id']],
           'owner': user4['auth_user_id']}
    data['dm'].append(dmi)
    assert dm_list_v1(user1['token']) == {
                                          'dms': [{'dm_id': 1, 'name': 'fidelcastro,enverhoxha'},
                                                        {'dm_id': 2, 'name': 'fidelcastro,thomassankara'}, 
                                                        {'dm_id': 3, 'name': 'thomassankara,fidelcastro,enverhoxha'}
                                                 ]
                                          } 


def test_no_dms():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    assert dm_list_v1(user1['token']) == {'dms': []}
