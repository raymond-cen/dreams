from src.data import data
from src.error import InputError, AccessError
from src.auth import decode_token

def admin_user_remove_v1(token, u_id):
    '''
    Removes a user. Their messages all become removed user and their handle str
    also becomes removed user.

    Arguments:
    <token> (<string>)    - <unique string for each login>
    <u_id> (<int>)    - <unique integer for each user>
    ...

    Exceptions:
    InputError  - Occurs when u_id does not refer to a valid user or they are the last owner
    AccessError - Occurs when user does not have correct permissions

    Return Value:
    Returns {}

    '''
    user_index = next((index for index, token_list in enumerate(data['users']) if token in token_list['token']), None)
    if user_index is None:
        raise InputError("Invalid token")
    if data['users'][user_index]['permission'] != 1:
        raise AccessError("The authorised user is not an owner")
    owner_count = 0
    all_ids = []
    for check_ids in data['users']:
        if check_ids['permission'] == 1:
            owner_count += 1
        all_ids.append(check_ids['auth_user_id'])
    if u_id not in all_ids:
        raise InputError("u_id does not refer to a valid user")
    if owner_count == 1 and decode_token(token) == u_id:
        raise InputError('The user is currently the only owner')

    for user_info in data['users']:
        if u_id == user_info['auth_user_id']:
            user_info['name_first'] = 'Removed'
            user_info['name_last'] = 'User'
            user_info['handle_str'] = 'Removed user'

    for message_info in data['message']['message_info']:
        if message_info['auth_user_id'] == u_id:
            message_info['message'] = 'Removed User'
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Changes a user's permissions to a regular member or owner.

    Arguments:
    <token> (<string>)    - <unique string for each login>
    <u_id> (<int>)    - <unique integer for each user>
    <permission_id> (<int>)    - <integer for which set of permissions>
    ...

    Exceptions:
    InputError  - Occurs when u_id does not refer to a valid user or permission id is not valid

    AccessError - Occurs when user does not have correct permissions

    Return Value:
    Returns {}

    '''
    if next((True for token_list in data['users'] if token in token_list['token']), False) is False:
        raise InputError("Invalid token")
    auth_user_id = decode_token(token)
    auth_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == auth_user_id), None)
    if data['users'][auth_index]['permission'] != 1:
        raise AccessError('The authorised user is not an owner')
    user_index = next((index for (index, d) in enumerate(data['users']) if d["auth_user_id"] == u_id), None)
    if user_index is None:
        raise InputError('u_id does not refer to a valid user')
    if permission_id == 1 or permission_id == 2:
        data['users'][user_index]['permission'] = permission_id
        return {}
    raise InputError('Invalid permission')