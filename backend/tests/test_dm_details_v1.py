import pytest

from src.auth import auth_register_v1
from src.dm import dm_details_v1
from src.channels import channels_create_v1
from src.error import InputError
from src.error import AccessError
from src.data import data

def clear_v1():
    for key in data:
        data[key] = []
def test_dm_d():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    dmi = {'dm_id': 1, 'dm_name': 'fidelcastro,enverhoxha',
           'u_ids': [user1['auth_user_id'], user2['auth_user_id']],
           'owner': user1['auth_user_id']}
    data['dm'].append(dmi)
    dmi = {'dm_id': 2, 'dm_name': 'enverhoxha,fidelcastro',
           'u_ids': [user1['auth_user_id'], user2['auth_user_id']],
           'owner': user2['auth_user_id']}
    data['dm'].append(dmi)
    assert dm_details_v1(user1['token'], 1) == {
                                                'name': 'fidelcastro,enverhoxha', 
                                                'members': [
                                                            {'u_id': 1, 
                                                            'email': 'castro@cuba.com', 
                                                            'name_first': 'fidel', 
                                                            'name_last': 'castro', 
                                                            'handle_str': 'fidelcastro'}, 
                                                            {'u_id': 2, 
                                                            'email': 'enver@bunker.com', 
                                                            'name_first': 'enver', 
                                                            'name_last': 'hoxha', 
                                                            'handle_str': 'enverhoxha'}]
                                                            }


def test_invalid_dm_id():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    with pytest.raises(InputError):
        assert dm_details_v1(user1['token'], 1)


def test_unauthorised_user():
    clear_v1()
    user1 = auth_register_v1('castro@cuba.com', 'revolution', 'fidel', 'castro')
    user2 = auth_register_v1('enver@bunker.com', 'bunkers', 'enver', 'hoxha')
    user3 = auth_register_v1('trotsky@traitor.com', 'icepick', 'leon', 'trotsky')
    dmi = {'dm_id': 1, 'dm_name': 'meghrajpatil,nandinisidnal',
           'u_ids': [user1['auth_user_id'], user2['auth_user_id']],
           'owner': user1['auth_user_id']}
    data['dm'].append(dmi)
    with pytest.raises(AccessError):
        assert dm_details_v1(user3['token'], 1)
